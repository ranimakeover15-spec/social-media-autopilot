"""
FFmpeg Transcoding Pipeline.
Converts any input video to standard mobile-optimized vertical reels:
- 1080x1920 9:16 vertical aspect ratio (auto-scaled and centered with black padding or crop)
- H.264 video codec (yuv420p pixel format, CRF 20, fast preset)
- AAC audio (192kbps, 44.1kHz stereo)
- +faststart flag (relocates moov atom to beginning of MP4 for instantaneous web streaming)
- Max 60-second duration enforcement
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from core.logger import logger
from core.config import config

class Transcoder:
    def __init__(self):
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """Validates that ffmpeg is installed and accessible."""
        if not shutil.which("ffmpeg"):
            logger.warning("⚠️ 'ffmpeg' binary was not found in system PATH. Please ensure FFmpeg is installed.")

    @staticmethod
    def get_media_info(file_path: Path) -> Dict[str, Any]:
        """Probes video metadata using ffprobe if available."""
        if not shutil.which("ffprobe"):
            return {}

        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(file_path)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(res.stdout)
        except Exception as e:
            logger.debug(f"ffprobe check failed on {file_path}: {e}")
            return {}

    def transcode(
        self,
        input_file: Path,
        output_file: Optional[Path] = None,
        max_duration: Optional[int] = None
    ) -> Path:
        """
        Transcodes the input video into high-compatibility 1080x1920 9:16 vertical MP4.
        """
        if not input_file.exists():
            raise FileNotFoundError(f"Input video does not exist: {input_file}")

        config.temp_dir.mkdir(parents=True, exist_ok=True)
        if output_file is None:
            output_file = config.temp_dir / f"transcoded_{input_file.stem}.mp4"

        duration_cap = max_duration or config.max_video_duration_sec

        logger.info(f"🎬 Transcoding video: {input_file.name} -> {output_file.name}")
        logger.info(f"⚙️ Target: {config.target_width}x{config.target_height} 9:16 | Codec: {config.video_codec} ({config.pixel_format}) | Audio: {config.audio_codec} ({config.audio_bitrate}) | +faststart")

        # FFmpeg filter: scale maintaining aspect ratio within 1080x1920 and pad with black margins
        # setsar=1 ensures square pixel ratio across all players
        vf_filter = (
            f"scale={config.target_width}:{config.target_height}:force_original_aspect_ratio=decrease,"
            f"pad={config.target_width}:{config.target_height}:(ow-iw)/2:(oh-ih)/2:black,"
            f"setsar=1"
        )

        cmd = [
            "ffmpeg",
            "-y", # overwrite output
            "-i", str(input_file),
            "-t", str(duration_cap), # Trim to max duration (e.g. 60s)
            "-vf", vf_filter,
            "-c:v", config.video_codec,
            "-preset", config.preset,
            "-crf", str(config.crf),
            "-pix_fmt", config.pixel_format,
            "-c:a", config.audio_codec,
            "-b:a", config.audio_bitrate,
            "-ar", str(config.audio_sample_rate),
            "-ac", "2",
            "-movflags", "+faststart",
            str(output_file)
        ]

        logger.debug(f"Running command: {' '.join(cmd)}")

        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            logger.error(f"❌ FFmpeg transcoding failed:\n{process.stderr}")
            raise RuntimeError(f"FFmpeg failed with return code {process.returncode}: {process.stderr[-500:]}")

        output_size_mb = output_file.stat().st_size / (1024 * 1024)
        logger.info(f"✅ Transcoding complete: {output_file.name} ({output_size_mb:.2f} MB)")
        return output_file

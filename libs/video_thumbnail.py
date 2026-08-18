#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
video_thumbnail.py

KEY_WORDS:      thumbnail video mp4 ffmpegthumbnailer subprocess
DESCRIPTION:    grab a single-frame thumbnail image from a video file by
                shelling out to ffmpegthumbnailer ( a small CLI built on
                the ffmpeg/libav libraries -- already installed here
                alongside vlc, no separate ffmpeg install needed ). no
                Qt dependency -- usable from any script, not just a tab
MORE:           ffmpegthumbnailer does its own seeking/decoding -- this
                is just a thin subprocess wrapper around it
"""


# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import subprocess


# ---- end imports


#-----------------------------------------------
def get_thumbnail( video_path, output_path, timestamp = "10%", size = 320, quality = 8 ):
    """
    what it says -- extract one frame from video_path and save it as an
    image at output_path ( image format is taken from output_path's
    extension -- .jpg/.png ). raises subprocess.CalledProcessError on
    failure ( e.g. bad video_path ), FileNotFoundError if
    ffmpegthumbnailer itself is not installed

        video_path      -- path to the source video
        output_path     -- path to write the thumbnail image to
        timestamp       -- "hh:mm:ss" absolute, or "NN%" percentage into the
                            video ( ffmpegthumbnailer's own -t option ). some
                            files ( odd container metadata, e.g. some phone
                            mp4s ) fail to seek and silently fall back to the
                            first frame instead of raising
        size            -- thumbnail size in pixels ( longest side ), 0 for
                            the video's original size
        quality         -- jpeg/png quality, 0 ( worst ) - 10 ( best )

        from video_thumbnail import get_thumbnail  #  get_thumbnail( video_path, output_path, timestamp = "10%", size = 320, quality = 8 )
    """
    command             = [
                            "ffmpegthumbnailer",
                            "-i", str( video_path ),
                            "-o", str( output_path ),
                            "-s", str( size ),
                            "-t", str( timestamp ),
                            "-q", str( quality ),
                            ]

    subprocess.run( command, check = True, capture_output = True )

# ---- eof

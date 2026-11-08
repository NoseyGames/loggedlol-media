# Motion Library media

Public preview-media mirror for Motion Library. Application source and prompt text stay in the separate private application repository.

The manifest records original source URLs, owning prompt IDs, MIME types, byte sizes, and SHA-256 digests. Asset filenames derive from the original URL. Original media attribution remains with MotionSites and the respective creators; no new license to the underlying media is granted by this mirror.

440 downloadable assets: 194 video files and 246 image files, including animated GIF previews. Some assets are reused across preview fields. Two additional image URLs returned HTTP 401 and could not be mirrored. Those failures remain explicit in `manifest.json`.

Two HLS previews were remuxed into standalone MP4s using the first/default video rendition, without re-encoding, and decode-tested. All other downloads preserve source bytes.

`mirror.py` downloads the non-HLS assets and checks every asset against the pinned SHA-256 manifest. Pre-remuxed MP4 files are committed directly. The manually runnable **Mirror preview media** workflow populates `assets/` and commits only after every expected file passes verification. It does not scrape paid content.

Use commit-pinned raw URLs for application playback:

`https://raw.githubusercontent.com/NoseyGames/motion-library-media/<commit>/assets/<filename>`

This is a snapshot, not an automatic recurring scrape. Source changes fail checksum validation instead of silently replacing media. Missing original images remain unavailable.

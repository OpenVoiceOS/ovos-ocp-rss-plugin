# OCP RSS Plugin

This plugin lets [OCP](https://github.com/OpenVoiceOS/ovos-media) play RSS feeds. It reads a feed URL, finds the first entry with an audio link, and returns that link as a playable stream.

## Install

```bash
pip install ovos-ocp-rss-plugin
```

## Usage

OCP loads this plugin through the `opm.ocp.extractor` entry point and calls it when a stream URI starts with the `rss` prefix. You can also call the extractor directly:

```python
from ovos_ocp_rss_plugin import OCPRSSFeedExtractor

stream = OCPRSSFeedExtractor.get_rss_first_stream(
    "rss//https://www.pbs.org/newshour/feeds/rss/podcasts/show"
)
# stream = {"duration": ..., "title": ..., "timestamp": ..., "uri": "..."}
```

`get_rss_first_stream` returns a dictionary with `duration`, `title`, `timestamp`, and `uri` for the first entry that has an audio link. It returns an empty dictionary if the feed has no such entry or cannot be read.

## Related projects

- [OpenVoiceOS/ovos-media](https://github.com/OpenVoiceOS/ovos-media), the OCP media player that loads this extractor
- [OpenVoiceOS/ovos-ocp-audio-plugin](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin), the voice media player that OCP stream extractors plug into
- [OpenVoiceOS/ovos-ocp-news-plugin](https://github.com/OpenVoiceOS/ovos-ocp-news-plugin), a sibling OCP stream extractor for news providers

## License

Apache-2.0

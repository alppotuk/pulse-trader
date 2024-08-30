# PulseTrader

PulseTrader is an ambitious project of mine that aims to provide an automated system that listens to some news sources (rss feeds, x, web scraping...), analyzes the sentiment of the news content, and identifies key companies mentioned. This data will be used to generate "pulses" -—messages that summarize the news and its potential buys or sells.

## Current Features

- RSSFeedListener: Actively listens to RSS feeds, fetching and processing new entries and creating Pulse Objects.
- Logger: Keeps track of events and errors, helping to monitor the system.
- Pulse: Represents the core unit of data, including content, sentiment analysis, and company identification.
- PulseAdapter: Serves as the backbone as an abstract class for integrating various data sources into the PulseTrader system.

## Under Construction

While the foundation has been laid with the development of key components, PulseTrader is far from complete. I'm working on enhancing the system's capabilities and refining its performance.

## Architecture

We've included a .drawio file in the repository that provides a visual template of the system's architecture. This will give you an idea of how the components interact and how the system is intended to function once it's fully operational. I did try to design it considering GoF patterns and so on. I am currently open for any progressive suggestions so do not hesistate to reach out.

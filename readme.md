# NZBGet PushBits Notifications Extension

## Overview

This extension for NZBGet allows users to send notifications via PushBits when new NZB are queued, NZB downloads are completed or encounter errors. PushBits is a relay server for push notifications. It enables you to send notifications via a simple web API, and delivers them to you through Matrix.

For more information about PushBits, visit their [GitHub repository](https://github.com/pushbits/server).

## Requirements
 - This script requires Python3.8 to be installed on your system.
 - "Requests" dependency needs to be installed. Install with "pip install requests".
 - A running Pushbits instance. 

## Installation

1. **Download Extension**: Obtain the latest version of the extension from the [GitHub repository](https://github.com/Richy1989/nzbget-pushbits-notification).

2. **Extract Files**: Extract the contents of the downloaded archive to a location of your choice.

3. **Copy Files**: Copy the extracted files to your NZBGet extension directory. Typically, this directory is configured with the variable `$ScriptDir`.

4. **Configure NZBGet**: Open the NZBGet web interface and navigate to Settings > Extensions Manager > PushBit Notifier.

5. **Configure PushBits**: Configure the `ConnectionString`, `AppToken` and specify the events to listen to. 

6. **Save Changes**: After configuring the PushBits extension, don't forget to click "Save all changes" to apply your settings.

## Usage

Once the extension is installed and configured, NZBGet will automatically send notifications to PushBits when new NZBs are queued, downloads are completed or encounter errors. You can receive these notifications on your configured Matrix account.

## Support and Contribution

For any issues with the extension, you can report them on the [GitHub repository](https://github.com/Richy1989/nzbget-pushbits-notification/issues). Contributions, such as bug fixes or feature enhancements, are welcome via pull requests.

## License

This extension is distributed under the [MIT License](MIT-LICENSE). Feel free to modify and distribute it according to the terms of this license.

---

**Disclaimer**: This extension is not officially associated with NZBGet or PushBits. Use it at your own risk.
# Mailchimp Campaign Bulk Replication
This Python script allows for easy and repetitive bulk replication of Mailchimp campaigns. 

The driver for this script can either be a CSV or Excel file where details for replicating a campaign is provided.

As of now, the following information will be updated in the replicated campaign:
* Campaign Title
* Campaign Subject Line
* Campaign Sender Name
* Campaign Reply To Email
* Campaign Recipient List
* Replicated campaign will be scheduled

To aid in troubleshooting, a log file is generated every run.

# Source File
As mentioned CSV or Excel can be supplied to the application. The application now allows the user to select and upload their file.

Please see example below for content expected in file. Also, headers are expected in the file. The schedule date and time **must** be in MM/DD/YYYY HH:MI AM/PM format.

|CampaignToDuplicate|CampaignTitle|SubjectLine|FromName|ReplyTo|ListName|ScheduleDateTime|
|-------------------|-------------|-----------|--------|-------|--------|----------------|
|Dummy Campaign To Duplicate|My Campaign Title|My Subject Line|John Smith|jsmit@example.com|Audience List Name|MM/DD/YYYY HH:MI AM/PM|

# Set Up
An Mailchimp API key will need to be created. For details on how to generate an API key, checkout Mailchimp's [tutorial](https://mailchimp.com/help/about-api-keys/).

# Mailchimp Campaign Replication

This Python script enables bulk replication of Mailchimp campaigns. 

The driver for this script is a CSV file where user(s) will provide details about which campaign to replicate, and the configurations of the replicated campaign(s).

As of now, the following information will be updated in the repliated campaign:
* Campaign Title
* Campaign Subject Line
* Campaign Sender Name
* Campaign Reply To Email
* Campaign Recipient List

The campaign can be scheduled, but that portion of the code is currently removed.

If the code for scheduling the campaign is enabled, the schedule date / time must follow the format *M/DD/YYYY HH:MM AM|PM*.

# Set Up
An Mailchimp API key will need to be created. For details on how to generate an API key, checkout Mailchimp's [tutorial](https://mailchimp.com/help/about-api-keys/).

# MailChimp Campaign Replication

This Python script enables bulk replication of MailChimp campaigns. 

The driver for this script is a CSV file where user(s) will provide details about which campaign to replicate, and the configurations of the replicated campaign(s).

As of now, the following information will be updated in the repliated campaign:
* Campaign Title
* Campaign Subject Line
* Campaign Sender Name
* Campaign Reply To Email
* Campaign Recipient List

The campaign can be scheduled, but that portion of the code is currently removed.

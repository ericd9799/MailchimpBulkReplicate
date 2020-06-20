#!/usr/bin/env python
# coding: utf-8
from mailchimp3 import MailChimp
import pandas as pd
import pytz
import datetime as dt
import logging
import os
import config

print(dt.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " - Running")

logFile = 'MailChimp_Campaign_Log_'+dt.datetime.now().strftime("%m%d%Y")+'.log'
logging.basicConfig(filename=os.path.expanduser('~')+'\\Desktop\\MailChimp_Scheduler\\Logs\\'+logFile, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", filemode='w', level=logging.INFO)

logger = logging.getLogger(__name__)
fileHandler = logging.FileHandler(filename=os.path.expanduser('~')+'\\Desktop\\MailChimp_Scheduler\\Logs\\'+logFile)
logger.addHandler(fileHandler)

try:
    config = pd.read_csv(os.path.expanduser('~')+'\\Desktop\\MailChimp_Scheduler\\Source\\config.csv', sep=',')
except FileNotFoundError as e:
    logger.error(str(e))
except Exception as e:
	logger.error(str(e))
else:
    logger.info("Config opened and read.")


try:
    df = pd.read_csv(os.path.expanduser('~')+'\\Desktop\\MailChimp_Scheduler\\Source\\MailChimpDuplicate.csv', sep=',', encoding = "ISO-8859-1")
except FileNotFoundError as e:
    logger.error(str(e))
except Exception as e:
	logger.error(str(e))
else:
    logger.info("Source CSV opened and read.")

client = MailChimp(mc_api=config['MailChimpAPIKey'][0], mc_user=config['MailChimpUser'][0])

# Retrieve list/audience within MailChimp
try:
    audience = client.lists.all(get_all=True, fields="lists.name,lists.id")
except Exception as e:
    logger.error("Unable to retrieve audience - " + str(e))
    raise
except AttributeError as e:
    logger.error(str(e))
    raise
else:
    logger.info("Retrieved all list/audience.")

for x in range(len(df)):
    logger.info("=====Starting: "+df.iloc[x]['CampaignTitle']+"=====")
    # Find the campaign to duplicate and retrieve the id
    try:
        campaignToDuplicateResult = client.search_campaigns.get(query=df.iloc[x]['CampaignToDuplicate'])
        
        if campaignToDuplicateResult['total_items'] == 0:
            logger.error("Did not find campaign to duplicate.")
            raise SystemExit
        
        campaignToDuplicateId = campaignToDuplicateResult['results'][0]['campaign']['id']
    except Exception as e:
        logger.error("Did not find campaign to duplicate - " + str(e))
        raise
    except AttributeError as e:
        logger.error(str(e))
        raise
    else:
        logger.info("Found campaign to duplicate.")
    
    # Duplicate the campaign
    try:
        duplicatedCampaign = client.campaigns.actions.replicate(campaign_id=campaignToDuplicateId)
    except Exception as e:
        logger.error("Unable to replicate campaign - " + str(e))
        raise
    except AttributeError as e:
        logger.error(str(e))
        raise
    else:
        logger.info("Duplication successful.")
    
    # Retrieve the id for the list to be receipient of campaign
    logger.info("Searching for list to retrieve ID.")
    listID = next(item['id'] for item in audience['lists'] if item['name'] == df.iloc[x]['ListName'])
    
    # Update the settings and receipient of the duplicated campaign according to spreadsheet
    try:
        client.campaigns.update(campaign_id = duplicatedCampaign['id'], data={
                'settings':{
                    'title':df.iloc[x]['CampaignTitle'],
                    'subject_line':df.iloc[x]['SubjectLine'],
                    'from_name':df.iloc[x]['FromName'], 
                    'reply_to':df.iloc[x]['ReplyTo']
                },
                'recipients':{
                    'list_id': listID,
                    'list_name':df.iloc[x]['ListName']
                }
            }
        )
    except Exception as e:
        logger.error("Unable to update campaign settings - " + str(e))
        raise
    except AttributeError as e:
        logger.error(str(e))
        raise
    else:
        logger.info("Settings and recipients update successful.")
		
	# Remove below code for initial release to allow quality checking
    # Convert time to UTC to schedule campaign
    scheduleDateTime = df.iloc[x]['ScheduleDateTime']
    unawareTimeZone = dt.datetime.strptime(scheduleDateTime, "%m/%d/%Y %I:%M %p")

    localtz = pytz.timezone('US/Eastern')
    awareTimeZone = localtz.localize(unawareTimeZone)

    utcDateTime = awareTimeZone.astimezone(pytz.utc)
    
    # Schedule the campaign
    try:
        client.campaigns.actions.schedule(duplicatedCampaign['id'], data={'schedule_time':utcDateTime})
    except Exception as e:
        logger.error("Unable to schedule campaign - " + str(e))
        raise
    except AttributeError as e:
        logger.error(str(e))
        raise
    else:
        logger.info("Update campaign schedule successful.")

    logger.info("=====End: "+df.iloc[x]['CampaignTitle']+"=====")

print(dt.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p") + " - Complete")
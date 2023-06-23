# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import packages
import pandas as pd

#import csv from desktop
data = pd.read_csv('/Users/sara.stavaski/Desktop/MGN/serverData.csv')
df = pd.read_csv('/Users/sara.stavaski/Desktop/MGN/mgnheaders.csv')
#variables
account_id = "881939749583"
region = "eu-west-1"
wave_name = "Wave 5"
wave_tag = "5"
wave_description = "This wave is aligned with all test systems"
app_tag = "App Tag 1"
app_description = "Description of the App"
subnet_id = "subnet-0c1b83b5d9671c1a6"
fqdn_for_action_framework = ""
network_interface_id = ""
subnet_id = "subnet-0d21568fc0f8ff294"
windows_security_group = "sg-0c741832dba26a62e"
linux_security_group = "sg-013d812295f725a6a"
security_group_2 = ""
volume_type = "gp3"
mgn_server_id = ""
private_ip = ""
instance_profile = ""

    
# display column names
data.columns.values

def transform_data(data, df, account_id, region, wave_name, wave_tag, wave_description, subnet_id, fqdn_for_action_framework, network_interface_id, windows_security_group, linux_security_group, security_group_2, volume_type, mgn_server_id, private_ip, instance_profile):

    #remove unneccesary columns from Evolve data
    data.drop(['Annual\rStorage\rCost','Used\rStorage\rGB', 'Initial\rShared \rTenancy \rInstance', 
               'Remapped\rShared\rTenancy\rInstance','Shared\rInstance\rRemapped', 'vCPUs \rfor \rPacking',
               'Shared\rvCPUs', 'Shared/DH\rOptimize\rCPU', 'Shared\rRAM','Physical/\rVirtual','SQL \rVersion',
               'SQL\rEdition', 'WS\rVersion', 'WS\rEdition',"SQL \rLic's \rReq'd", 'Shared\rSQL Server \rLicense \rType',
               'DH\rSQL Server \rLicense \rType','On-Prem\rvCPU/\rCores','On-Prem \rAvg CPU \rUtilization%',
               'On-Prem \rPeak CPU \rUtilization%', 'On-Prem\rRAM\r(GB)','On-Prem\rAvg RAM \rUtilization%',
               'On-Prem\rPeak RAM \rUtilization%','On-Prem\r%Uptime \r(continuous)', 'Shared\rAnnualized \r3YR NURI',
               'Shared\rAnnualized \rPowerMgt', 'Final\rDH Host\r#','Instance\rRemapped\rFrom DH\rPlacement',
               'Final DH/\rShared\rInstance \rFamily','Final DH/\rShared \rInstance \rSize', 'App Group','Migration Strategy',
               'OS','Lic SQL By', 'Lic WS\rBy'
               ], inplace=True, axis=1)
    #rename columns 
    data.rename(columns = {'Final\rInstance\rType':'mgn:launch:instance-type','Guest OS':'mgn:server:platform',
                           'Environment':'mgn:server:tag:Environment', 'Final\rInstance\rTenancy':'mgn:launch:placement:tenancy',
                           'ServerName':'mgn:server:tag:Name', 'Application':'mgn:app:name', 'Owner':'mgn:server:tag:Owner',
                           'Team':'mgn:server:tag:Team'
                           }, inplace=True)


    # add and editcolumns for mgn import 
    data['mgn:server:platform'] = data['mgn:server:platform'].str.upper()
    data["mgn:launch:placement:tenancy"] = data["mgn:launch:placement:tenancy"].replace("Shared", "default")
    data["mgn:launch:placement:tenancy"] = data["mgn:launch:placement:tenancy"].replace("DH", "host")
    data.loc[data["mgn:server:platform"] == "WINDOWS", "mgn:launch:nic:0:security-group-id:0"] = windows_security_group
    data.loc[data["mgn:server:platform"] == "LINUX", "mgn:launch:nic:0:security-group-id:0"] = linux_security_group

    # add evolve data to df 
    df['mgn:launch:instance-type'] = data['mgn:launch:instance-type']
    df['mgn:server:platform'] = data['mgn:server:platform']
    df['mgn:server:tag:Environment'] = data['mgn:server:tag:Environment']
    df['mgn:launch:placement:tenancy'] = data['mgn:launch:placement:tenancy']
    df['mgn:server:tag:Name'] = data['mgn:server:tag:Name']
    df['mgn:app:name'] = data['mgn:app:name']
    df['mgn:server:tag:Owner'] = data['mgn:server:tag:Owner']
    df['mgn:server:tag:Team'] = data['mgn:server:tag:Team']
    
    # add defined prameters to columns 
    df["mgn:account-id"] = account_id
    df["mgn:region"] = region
    df["mgn:wave:name"] = wave_name
    df["mgn:wave:tag:Wave"] = wave_tag
    df["mgn:wave:description"] = wave_description
    df["mgn:app:tag:AppTag"] = app_tag
    df["mgn:app:description"] = app_description
    df["mgn:server:platform"] = data["mgn:server:platform"]
    df["mgn:launch:nic:0:subnet-id"] = subnet_id
    df["mgn:server:fqdn-for-action-framework"] = fqdn_for_action_framework
    df["mgn:launch:nic:0:network-interface-id"] = network_interface_id
    df["mgn:launch:nic:0:security-group-id:1"] = security_group_2
    df["mgn:launch:nic:0:private-ip:0"] = private_ip
    df["mgn:launch:tag:instance:Name"] = df["mgn:server:tag:Name"]
    df["mgn:launch:iam-instance-profile:name"] = instance_profile
    df.loc[df["mgn:server:platform"] == "LINUX", "mgn:launch:volume:/dev/xvda:type"] = volume_type
    df.loc[df["mgn:server:platform"] == "WINDOWS", "mgn:launch:volume:c:0:type"] = volume_type
    df["mgn:server:id"] = mgn_server_id

    return df



transformed_df = transform_data(data, df, account_id, region, wave_name, wave_tag, wave_description, subnet_id, fqdn_for_action_framework, network_interface_id, windows_security_group, linux_security_group, security_group_2, volume_type, mgn_server_id, private_ip, instance_profile)

transformed_df.to_csv('/Users/sara.stavaski/Desktop/MGN/transformed_data.csv', index=False)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:54:09 2023

@author: sara.stavaski
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import packages
import pandas as pd
import random

#import csv from desktop
data = pd.read_csv('/Users/sara.stavaski/Desktop/MGN/serverData.csv')
df = pd.read_csv('/Users/sara.stavaski/Desktop/MGN/templateHeaders.csv')
#variables
instance_type_right_sizing = "NONE"
subnet_id = ["subnet-0d21568fc0f8ff294", "subnet-0c1b83b5d9671c1a6", "subnet-0d9ba324dbbb0fb39"]
security_group_1 = "sg-0c741832dba26a62e"
security_group_2 = "sg-013d812295f725a6a"
copy_private_ip	= "FALSE"
start_instance_upon_launch = "STOPPED"
transfer_server_tags = "TRUE"
boot_mode = ""
primary_private_ip = ""
eni = ""
volume_type = "gp3"
volume_throughput = "125"
volume_iops = "3000"
placement_group_name = ""
host_resource_group_arn = ""
host_id = ""


    
# display column names
data.columns.values
def format_resource_tags(row):
    return f"Environment:{row['Environment']},Application:{row['Application']},Team:{row['Team']}"

def transform_data(data, df, instance_type_right_sizing, subnet_id, security_group_1, security_group_2, copy_private_ip, 
                   start_instance_upon_launch, transfer_server_tags, boot_mode, primary_private_ip, eni, volume_type, 
                   volume_throughput, volume_iops, placement_group_name, host_resource_group_arn, host_id):

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
               'OS','Lic SQL By'
               ], inplace=True, axis=1)
    #rename columns 
    data.rename(columns = {'Final\rInstance\rType':'EC2_Instance_type','Guest OS':'OS','Final\rInstance\rTenancy':'Tenancy',
                           'ServerName':'Server_Name', 
                           }, inplace=True)


    # create new df with properformat for to run in script: https://github.com/aws-samples/aws-mgn-launchtemplate-manager/blob/main/target-templates-import/target_templates_import.py
    df['Server_Name'] = data['Server_Name']
    df["OS"] = data["OS"]
    df["Instance_type_right_sizing"] = instance_type_right_sizing
    df['EC2_Instance_type'] = data['EC2_Instance_type']
    random.shuffle(subnet_id)
    df["Subnet_ID"] = random.choices(subnet_id, k=len(df))
    df["Security_Groups"] = f"0:{security_group_1},1:{security_group_2}"
    df["Copy_private_ip	"] = copy_private_ip	
    df["Start_Instance_upon_launch"] = start_instance_upon_launch
    df["Transfer_Server_tags"] = transfer_server_tags
    df["OS_licensing_byol"] = data["Lic WS\rBy"].map({"WS LI": "FALSE", "WS BYOL": "TRUE"})
    df["Boot_mode"] = "boot_mode" 
    df["Primary_private_ip"] = primary_private_ip
    df["ENI"] = eni
    df.loc[df["OS"] == "Windows", "volume_type"] = "c:0:" + volume_type
    df.loc[df["OS"] == "Linux", "volume_type"] = "/dev/xvda:" + volume_type
    df.loc[df["OS"] == "Windows", "volume_throughput"] = "c:0:" + volume_throughput
    df.loc[df["OS"] == "Linux", "volume_throughput"] = "/dev/xvda:" + volume_throughput
    df.loc[df["OS"] == "Windows", "volume_iops"] = "c:0:" + volume_iops
    df.loc[df["OS"] == "Linux", "volume_iops"] = "/dev/xvda:" + volume_iops
    df["Resource_Tags"] = data.apply(format_resource_tags, axis=1)
    df["placement_group_name"] = placement_group_name
    df["Tenancy"] = data["Tenancy"].replace("Shared", "default")
    df["Tenancy"] = data["Tenancy"].replace("DH", "host")
    df["HostresourceGroupArn"] = host_resource_group_arn
    df["HostId"] = 	host_id
    
 
    return df



transformed_df = transform_data(data, df, instance_type_right_sizing, subnet_id, security_group_1, security_group_2, 
                                copy_private_ip, start_instance_upon_launch, transfer_server_tags, boot_mode, primary_private_ip, 
                                eni, volume_type, volume_throughput, volume_iops, placement_group_name, 
                                host_resource_group_arn, host_id)

transformed_df.to_csv('/Users/sara.stavaski/Desktop/MGN/transformed_data.csv', index=False)

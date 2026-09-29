import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Analysis of Ofgem Innovation Projects")
st.write("This analysis provides insight into previous and current Innovation Projects funded by Ofgem.\
         Data regarding these projects, accessed using Energy Networks Association's Smarter Networks Portal,\
         is accessible through a series of different visual and graphical means, and adjustable to the users demand.\
         Information regarding the analyses conducted and methods used can be found with each plot.")

#Import the datafile
data = pd.read_excel('snp_dataset_useful.xlsx')
#Extract the required data from the datafile
#Time
start_date = data['Project Start Date']
end_date = data['Project End Date']
status = data['Project Status']
#Funding & Association
budget = data['Project Budget']
owners = data['Owner Network']
collaborators = data['Collaborating Networks']
funding_mechanism = data['Funding Mechanism']
#Area of research
strategy = data['Strategy Theme']
research = data['Research Areas']
technology = data['Technology Areas']
sector = data['Lead Sector']
secondary_sectors = data['Other Related Sectors']

#Determine the time difference between the start and end dates
start_dt = pd.to_datetime(start_date, format="%d/%m/%Y", errors='coerce')
end_dt = pd.to_datetime(end_date, format="%d/%m/%Y", errors='coerce')
time_difference = end_dt - start_dt
durations = time_difference.dt.days

#For the projects involved in multiple sectors, make sure they are included in each sector list
sector_types = sector.unique()
sector_types = sector_types[:4]
sector_types_idx = [sector[sector.str.contains(st, na=False)].index.tolist() for st in sector_types]

#Do the same for technology as well
technology_types =['Active Network Management', 'Asset Management', 'Biomethane', 'Carbon Emission Reduction Technologies',\
                   'Commercial', 'Comms and IT', 'Community Schemes', 'Condition Monitoring', 'Conductors', 'Control Systems',\
                   'Cyber Security', 'Demand Response', 'Demand Side Management', 'Digital Network', 'Distributed Generation',\
                   'Electric Vehicles', 'Electricity Transmission Networks', 'Energy Storage', 'Energy Storage and Demand Response',\
                   'Environmental', 'Fault Current', 'Fault Level', 'Fault Management', 'Gas Distribution Networks',\
                   'Gas Transmission Networks', 'Gas Vehicles', 'Green Gas', 'HVDC', 'Harmonics', 'Health and Safety', 'Heat Pumps',\
                   'High Voltage Technology', 'Hydrogen', 'LV & 11kV Networks', 'Low Carbon Generation', 'Maintenance & Inspections',\
                   'Measurement', 'Meshed Networks', 'Modelling', 'Network Automation', 'Network Monitoring', 'Offshore Transmission',\
                   'Overhead Lines', 'Photovoltaics', 'Poverty', 'Pre-Heat', 'Protection', 'Resilience', 'Stakeholder Engagement',\
                   'Storage', 'Substation Monitoring', 'Substations', 'System Security', 'Transformers', 'Voltage Control']
                   
technology_types_idx = [technology[technology.str.contains(tt, na=False)].index.tolist() for tt in technology_types]

st.subheader("Plot of Total Project Budgets vs Sector (use as test)")
total_sector_budget = np.zeros(len(sector_types))
for i in range(len(sector_types)):
  for j in range(len(sector_types_idx[i])):
    total_sector_budget[i] += budget[sector_types_idx[i][j]]

fig = px.bar(x=sector_types, y=total_sector_budget, labels={'x':'Sector', 'y':'Total Funding (£)'})
st.write(fig)

st.subheader("Plot of Total Project Budgets vs Technology (use as test)")
total_technology_budget = np.zeros(len(technology_types))
for i in range(len(technology_types)):
  for j in range(len(technology_types_idx[i])):
    total_technology_budget[i] += budget[technology_types_idx[i][j]]
fig1 = px.bar(x=technology_types, y=total_technology_budget, labels={'x':'Technology', 'y':'Total Funding (£)'})
st.write(fig1)

st.write("Last updated 29/09/2026")
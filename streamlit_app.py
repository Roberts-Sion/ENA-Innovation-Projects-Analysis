import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

st.subheader('(Other test plot)')
start_dt_sort = np.sort(start_dt)
total_cumul = [np.sum(start_dt_sort <= date) for date in start_dt_sort]
end = 0
while end == 0:
  remove = total_cumul.pop()
  end = remove
  if end == 0:
    continue
  else:  
    total_cumul.append(remove)
sector_cumul = {}
for st in sector_types:
  sector_idx = sector[sector.str.contains(st, na=False)].index
  sector_dates = start_dt.loc[sector_idx]
  sector_cumul[st] = [np.sum(sector_dates.values <= date) for date in start_dt_sort]
  end = 0
  while end == 0:
    remove = sector_cumul[st].pop()
    end = remove
    if end == 0:
      continue
    else:  
      sector_cumul[st].append(remove)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=start_dt_sort, y=total_cumul, mode='lines+markers', name='Total'))
for st in sector_types:
  fig2.add_trace(go.Scatter(x=start_dt_sort, y=sector_cumul[st], mode='lines+markers', name=st, visible=False))

buttons = []
buttons.append(dict(label='Total', method='update', args=[{'visible': [True] + [False]*len(sector_types)}, {'title': 'Cumulative Number of All Projects'}]))
for i, st in enumerate(sector_types):
  visible = [False] * (len(sector_types) + 1)
  visible[i+1] = True
  buttons.append(dict(label=st, method='update', args=[{'visible': visible}, {'title': f'Cumulative Number of {st} Projects'}]))

fig2.update_layout(updatemenus=[dict(buttons=buttons, direction='down', showactive=True, x=0, xanchor='left', y=1.12, yanchor='top')],\
                  xaxis_title='Date (DD-MM-YY)', yaxis_title='Number of Projects', title='Cumulative Number of Projects', hovermode='x unified')
st.plotly_chart(fig2, use_container_width=True)

st.write("Last updated 29/09/2026")
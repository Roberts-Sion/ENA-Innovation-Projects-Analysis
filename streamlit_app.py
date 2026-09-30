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
titles = data['Project Title']
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

#Do the same for owners as well
owner_types = owners.unique()
owner_types = [ot for ot in owner_types if pd.notna(ot)]
owner_types_idx = [owners[owners.str.contains(ot, na=False)].index.tolist() for ot in owner_types]

#Do the same for technology as well
technology_types = technology.unique()
technology_types = [tt for tt in technology_types if pd.notna(tt)]
technology_types_idx = [technology[technology.str.contains(tt, na=False)].index.tolist() for tt in technology_types]

st.subheader("Plot of Total Project Budgets vs Sector (use as test)")
total_sector_budget = np.zeros(len(sector_types))
for i in range(len(sector_types)):
  for j in range(len(sector_types_idx[i])):
    total_sector_budget[i] += budget[sector_types_idx[i][j]]
bts_total_sector_budget_idx = np.argsort(total_sector_budget)[::-1]
bts_total_sector_budget = total_sector_budget[bts_total_sector_budget_idx]
bts_sector_types = np.array(sector_types)[bts_total_sector_budget_idx]
fig = px.bar(x=bts_sector_types, y=bts_total_sector_budget, labels={'x':'Sector', 'y':'Total Funding (£)'})
st.write(fig)
sector_names = ["Electricity Distribution", "Electricity Transmission", "Gas Distribution", "Gas Transmission"]
sector_indices = {"Electricity Distribution": sector_types_idx[0], "Electricity Transmission": sector_types_idx[1],\
                  "Gas Distribution": sector_types_idx[2], "Gas Transmission": sector_types_idx[3]}
tables = {}
for sect in sector_names:
  indices = sector_indices[sect]
  tables[sect] = pd.DataFrame({"Project Title": titles.iloc[indices].values,\
                                 "Technology Areas": technology.iloc[indices].values,\
                                 "Project Budget": budget.iloc[indices].values,\
                                 "Funding Mechanism": funding_mechanism.iloc[indices].values})
if "selected_sector" not in st.session_state:
  st.session_state.selected_sector = None
for sect in sector_names:
  if st.button(f"Show Table ({sect})", key=f"button_{sect}"):
    st.session_state.selected_sector = sect
if st.session_state.selected_sector is not None:
  selected_sector = st.session_state.selected_sector
  st.subheader(selected_sector)
  st.dataframe(tables[selected_sector], use_container_width=True, hide_index=True)

st.subheader("Plot of Total Project Budgets vs Owner (use as test)")
total_owner_budget = np.zeros(len(owner_types))
for i in range(len(owner_types)):
  for j in range(len(owner_types_idx[i])):
    total_owner_budget[i] += budget[owner_types_idx[i][j]]
bts_total_owner_budget_idx = np.argsort(total_owner_budget)[::-1]
bts_total_owner_budget = total_owner_budget[bts_total_owner_budget_idx]
bts_owner_types = np.array(owner_types)[bts_total_owner_budget_idx]
fig1 = px.bar(x=bts_owner_types, y=bts_total_owner_budget, labels={'x':'Owner', 'y':'Total Funding (£)'})
st.write(fig1)

st.subheader("Plot of Total Project Budgets vs Technology (use as test)")
total_technology_budget = np.zeros(len(technology_types))
for i in range(len(technology_types)):
  for j in range(len(technology_types_idx[i])):
    total_technology_budget[i] += budget[technology_types_idx[i][j]]
bts_total_technology_budget_idx = np.argsort(total_technology_budget)[::-1]
bts_total_technology_budget = total_technology_budget[bts_total_technology_budget_idx]
bts_technology_types = np.array(technology_types)[bts_total_technology_budget_idx]
fig2 = px.bar(x=bts_technology_types, y=bts_total_technology_budget, labels={'x':'Technology', 'y':'Total Funding (£)'})
fig2.update_layout(width=2500, height=800)
fig2.update_xaxes(tickmode='linear', dtick=75, tickangle=20, tickfont=dict(size=8))
st.write(fig2)

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
for sc in sector_types:
  sector_idx = sector[sector.str.contains(sc, na=False)].index
  sector_dates = start_dt.loc[sector_idx]
  sector_cumul[sc] = [np.sum(sector_dates.values <= date) for date in start_dt_sort]
  end = 0
  while end == 0:
    remove = sector_cumul[sc].pop()
    end = remove
    if end == 0:
      continue
    else:  
      sector_cumul[sc].append(remove)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=start_dt_sort, y=total_cumul, mode='lines+markers', name='Total'))
for sc in sector_types:
  fig3.add_trace(go.Scatter(x=start_dt_sort, y=sector_cumul[sc], mode='lines+markers', name=sc, visible=False))

buttons = []
buttons.append(dict(label='Total', method='update', args=[{'visible': [True] + [False]*len(sector_types)}, {'title': 'Cumulative Number of All Projects'}]))
for i, sc in enumerate(sector_types):
  visible = [False] * (len(sector_types) + 1)
  visible[i+1] = True
  buttons.append(dict(label=sc, method='update', args=[{'visible': visible}, {'title': f'Cumulative Number of {sc} Projects'}]))

fig3.update_layout(updatemenus=[dict(buttons=buttons, direction='down', showactive=True, x=0, xanchor='left', y=1.12, yanchor='top')],\
                  xaxis_title='Date (DD-MM-YY)', yaxis_title='Number of Projects', title='Cumulative Number of Projects', hovermode='x unified')
st.plotly_chart(fig3, use_container_width=True)

st.write("Last updated 30/09/2026")
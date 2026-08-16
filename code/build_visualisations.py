"""
VDS 2025/26 Second Chance Project - Earthquakes
Builds 4 interactive visualisations (Plotly -> HTML).
Usage: python build_visualisations.py path/to/earthquakes.csv
"""
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CSV = sys.argv[1] if len(sys.argv) > 1 else "earthquakes-2000-01-01-2023-02-12.csv"

# ---------- shared prep ----------
df = pd.read_csv(CSV, usecols=["time","latitude","longitude","depth","mag","magType","place","type"])
df = df[df["type"] == "earthquake"].copy()
df["time"] = pd.to_datetime(df["time"], format="mixed")
df["year"], df["month"], df["day"] = df["time"].dt.year, df["time"].dt.month, df["time"].dt.day
df["region"] = df["place"].str.split(", ").str[-1].str.strip()
df.loc[df["region"] == "CA", "region"] = "California"
df["depth"] = df["depth"].clip(lower=0)
df["depth_class"] = pd.cut(df["depth"], [-0.1, 70, 300, 1000],
                           labels=["Shallow (<70 km)","Intermediate (70-300 km)","Deep (>300 km)"])
df["mag_class"] = pd.cut(df["mag"], [0, 4, 5, 6, 10], labels=["<4","4-5","5-6","6+"])
df["date_str"] = df["time"].dt.strftime("%Y-%m-%d")

# ---------- Viz 1: Interactive Map Explorer ----------
d = df[df["mag"] >= 4.5]
years = sorted(d["year"].unique())

def map_trace(dd):
    return go.Scattergeo(
        lon=dd["longitude"], lat=dd["latitude"], mode="markers",
        marker=dict(size=(dd["mag"]-3.5)**2.1, color=dd["depth"], colorscale="Viridis_r",
                    cmin=0, cmax=700, colorbar=dict(title="Depth (km)"), opacity=0.55, line_width=0),
        customdata=np.stack([dd["mag"], dd["depth"], dd["date_str"], dd["place"].fillna("")], axis=-1),
        hovertemplate="<b>M %{customdata[0]}</b> | %{customdata[1]:.0f} km<br>%{customdata[2]}<br>%{customdata[3]}<extra></extra>")

fig = go.Figure(data=[map_trace(d[d["year"]==years[0]])],
                frames=[go.Frame(data=[map_trace(d[d["year"]==y])], name=str(y)) for y in years])
fig.update_layout(
    title="Earthquake Map Explorer (M \u2265 4.5) - size = magnitude, color = depth",
    geo=dict(projection_type="natural earth", showland=True, landcolor="#f0ede5",
             showocean=True, oceancolor="#dcecf5", coastlinecolor="#999"),
    updatemenus=[dict(type="buttons", showactive=False, x=0.05, y=-0.08, buttons=[
        dict(label="\u25b6 Play", method="animate",
             args=[None, dict(frame=dict(duration=600, redraw=True), fromcurrent=True)]),
        dict(label="\u23f8 Pause", method="animate",
             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])])],
    sliders=[dict(active=0, currentvalue=dict(prefix="Year: "), pad=dict(t=30),
        steps=[dict(method="animate", label=str(y),
                    args=[[str(y)], dict(frame=dict(duration=0, redraw=True), mode="immediate")])
               for y in years])],
    height=650, margin=dict(l=10, r=10, t=60, b=10))
fig.write_html("viz1_map_explorer.html", include_plotlyjs=True)

# ---------- Viz 2: Temporal Dashboard ----------
d = df[df["year"] < 2023]
piv = d.pivot_table(index="year", columns="mag_class", values="mag", aggfunc="count", observed=True).fillna(0)
colors = {"<4":"#c6dbef","4-5":"#6baed6","5-6":"#2171b5","6+":"#d62728"}
fig = make_subplots(rows=2, cols=1, row_heights=[0.45,0.55], vertical_spacing=0.14,
                    subplot_titles=("Events per year by magnitude class",
                                    "Daily activity calendar (select year below)"))
for c in ["<4","4-5","5-6","6+"]:
    fig.add_trace(go.Scatter(x=piv.index, y=piv[c], stackgroup="one", name=c,
                             line=dict(width=0.5, color=colors[c]), fillcolor=colors[c]), row=1, col=1)
years2 = sorted(d["year"].unique())
for y in years2:
    dy = d[d["year"] == y]
    cal = dy.pivot_table(index="day", columns="month", values="mag", aggfunc="count") \
            .reindex(index=range(1,32), columns=range(1,13))
    fig.add_trace(go.Heatmap(z=cal.values, x=list(range(1,13)), y=list(range(1,32)),
        colorscale="YlOrRd", visible=(y == 2018), showscale=True,
        colorbar=dict(title="# events", len=0.45, y=0.18),
        hovertemplate="Month %{x}, Day %{y}: %{z} events<extra></extra>"), row=2, col=1)
buttons = []
for i, y in enumerate(years2):
    vis = [True]*4 + [j == i for j in range(len(years2))]
    buttons.append(dict(label=str(y), method="update", args=[dict(visible=vis)]))
fig.update_layout(title="Temporal Dashboard: Earthquake Activity 2000-2022",
    updatemenus=[dict(buttons=buttons, x=1.0, y=0.42, xanchor="right", yanchor="bottom",
                      active=years2.index(2018))],
    height=850, hovermode="x unified", legend=dict(orientation="h", y=1.06, x=0.35))
fig.update_xaxes(title="Year", row=1, col=1); fig.update_yaxes(title="# events", row=1, col=1)
fig.update_xaxes(title="Month", row=2, col=1)
fig.update_yaxes(title="Day of month", autorange="reversed", row=2, col=1)
fig.write_html("viz2_temporal_dashboard.html", include_plotlyjs=True)

# ---------- Viz 3: Depth-Magnitude Explorer ----------
regions = ["All","Alaska","Indonesia","Chile","Japan","Tonga","Greece","California","Mexico","Puerto Rico"]
fig = make_subplots(rows=2, cols=2, column_widths=[0.8,0.2], row_heights=[0.2,0.8],
                    horizontal_spacing=0.02, vertical_spacing=0.02,
                    shared_xaxes=True, shared_yaxes=True)
for i, r in enumerate(regions):
    dd = df if r == "All" else df[df["region"] == r]
    if len(dd) > 15000: dd = dd.sample(15000, random_state=1)
    vis = (r == "All")
    fig.add_trace(go.Histogram(x=dd["mag"], nbinsx=50, marker_color="#b2182b",
                               visible=vis, showlegend=False), row=1, col=1)
    fig.add_trace(go.Scattergl(x=dd["mag"], y=dd["depth"], mode="markers",
        marker=dict(size=3, color="#b2182b", opacity=0.18), visible=vis, showlegend=False,
        hovertemplate="M %{x} | %{y:.0f} km<extra></extra>"), row=2, col=1)
    fig.add_trace(go.Histogram(y=dd["depth"], nbinsy=60, marker_color="#b2182b",
                               visible=vis, showlegend=False), row=2, col=2)
buttons = []
for i, r in enumerate(regions):
    vis = [False]*(3*len(regions))
    for k in range(3): vis[3*i+k] = True
    buttons.append(dict(label=r, method="update", args=[dict(visible=vis)]))
fig.update_layout(title="Depth vs Magnitude Explorer - select region (15k sample per view)",
    updatemenus=[dict(buttons=buttons, x=1.0, y=1.12, xanchor="right")], height=750, bargap=0.02)
fig.update_yaxes(autorange="reversed", title="Depth (km)", row=2, col=1)
fig.update_xaxes(title="Magnitude", row=2, col=1)
fig.write_html("viz3_depth_magnitude.html", include_plotlyjs=True)

# ---------- Viz 4: Depth-Class Small Multiples ----------
classes = ["Shallow (<70 km)","Intermediate (70-300 km)","Deep (>300 km)"]
fig = make_subplots(rows=1, cols=3,
    subplot_titles=[f"{c}<br>({(df['depth_class']==c).sum():,} events)" for c in classes],
    specs=[[{"type":"geo"}]*3], horizontal_spacing=0.01)
for i, c in enumerate(classes):
    dd = df[df["depth_class"] == c]
    if len(dd) > 25000: dd = dd.sample(25000, random_state=1)
    fig.add_trace(go.Scattergeo(lon=dd["longitude"], lat=dd["latitude"], mode="markers",
        marker=dict(size=2.2, color=["#2166ac","#f4a582","#b2182b"][i], opacity=0.35),
        showlegend=False, hovertemplate="M %{customdata[0]} | %{customdata[1]:.0f} km<extra></extra>",
        customdata=np.stack([dd["mag"], dd["depth"]], axis=-1)), row=1, col=i+1)
for g in ["geo","geo2","geo3"]:
    fig.layout[g].update(projection_type="natural earth", showland=True, landcolor="#f2efe9",
                         showocean=True, oceancolor="#e8f1f8", coastlinecolor="#aaa")
fig.update_layout(title="Earthquakes by Depth Class - deep events occur only along subduction zones",
                  height=420, margin=dict(l=10, r=10, t=90, b=10))
fig.write_html("viz4_small_multiples.html", include_plotlyjs=True)

print("Done: 4 HTML files written.")

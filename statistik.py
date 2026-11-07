import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def ringkasan(data):
    if data.empty:
        return 0, 0, 0, 0

    total = float(data["berat"].sum())
    organik = float(data.loc[data["kategori"] == "Organik", "berat"].sum())
    anorganik = float(data.loc[data["kategori"] == "Anorganik", "berat"].sum())
    b3 = float(data.loc[data["kategori"] == "B3", "berat"].sum())

    return total, organik, anorganik, b3


def grafik_kategori(data):
    hasil = data.groupby("kategori", as_index=False)["berat"].sum()

    # Hilangkan kategori dengan berat 0
    hasil = hasil[hasil["berat"] > 0]

    fig = px.pie(
        hasil,
        names="kategori",
        values="berat",
        hole=0.68,
        color="kategori",
        color_discrete_map={
            "Organik": "#10B981",
            "Anorganik": "#3B82F6",
            "B3": "#F59E0B"
        }
    )

    total = hasil["berat"].sum()

    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        marker=dict(
            line=dict(color="#0B1120", width=4)
        ),
        hovertemplate="<b>%{label}</b><br>%{value:.2f} KG<br>%{percent}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_dark",
        title="Komposisi Sampah",
        title_x=0.5,
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        annotations=[
            dict(
                text=f"<b>{total:.1f}</b><br>KG",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=26, color="#10B981")
            )
        ],
        margin=dict(t=65, b=40, l=40, r=40)
    )

    return fig


def grafik_bulanan(data):
    salinan = data.copy()

    salinan["tanggal"] = pd.to_datetime(salinan["tanggal"])
    salinan["bulan"] = salinan["tanggal"].dt.to_period("M").astype(str)

    hasil = salinan.groupby(
        "bulan",
        as_index=False
    )["berat"].sum()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=hasil["bulan"],
            y=hasil["berat"],
            marker=dict(
                color=hasil["berat"],
                colorscale=[
                    [0, "#065F46"],
                    [0.5, "#10B981"],
                    [1, "#34D399"]
                ],
                line=dict(
                    color="#34D399",
                    width=1
                )
            ),
            text=hasil["berat"].apply(
                lambda x: f"{x:.2f} KG"
            ),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Berat: %{y:.2f} KG<extra></extra>"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title="Perkembangan Sampah Bulanan",
        title_x=0.5,
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis_title="Bulan",
        yaxis_title="Berat Sampah (KG)",
        xaxis=dict(
            type="category",
            showgrid=False
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            rangemode="tozero"
        ),
        margin=dict(t=65, b=50, l=50, r=30),
        showlegend=False
    )

    return fig
import geopandas as gpd
import pandas as pd
import folium
import camelot
import numpy as np
import branca.colormap as cm


PDF_PAGES = ["5", "24", "43", "62", "81", "100", "119"]
PDF_FILE = "hamburg_report.pdf"
GEO_FILE = "hamburg.geojson"


def extract_data_from_pdf(file_name: str, pages: list[str]) -> pd.DataFrame:
    tables = []

    for page in pages:
        t = camelot.read_pdf(file_name, pages=page, flavor="stream")
        df = t[0].df
        df = df.drop(columns=[1, 2, 3, 5, 6, 7, 8])
        tables.append(df)

    return pd.concat(tables, ignore_index=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = ["neighborhood", "cases"]

    df["cases"] = (
        df["cases"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["cases"] = pd.to_numeric(df["cases"], errors="coerce")

    df = df[~df["neighborhood"].str.startswith("Bezirk", na=False)]
    df = df[df["neighborhood"] != "Stadtteile"]
    df = df.dropna(subset=["cases"])

    df["neighborhood"] = df["neighborhood"].replace({
        "Altstadt": "Hamburg-Altstadt",
        "Wohldorf-Ohlstedt": "Wohlsdorf-Ohlstedt",
        "Lemsahl-Mellingstedt": "Lehmsahl-Mellingstedt"
    })

    df["cases"] = df["cases"].fillna(0)

    return df.sort_values("cases", ascending=False)


def prepare_geodata(df: pd.DataFrame, geo_file: str) -> gpd.GeoDataFrame:
    geo = gpd.read_file(geo_file).to_crs(epsg=4326)

    geo = geo.merge(df, left_on="name", right_on="neighborhood", how="left")

    geo["cases"] = geo["cases"].fillna(0)
    geo["cases_display"] = geo["cases"].astype(int).map("{:,}".format)

    geo["cases_sqrt"] = np.sqrt(geo["cases"])

    return geo[["name", "cases", "cases_display", "cases_sqrt", "geometry"]]


def create_colormap(geo: gpd.GeoDataFrame):
    return cm.linear.YlOrRd_09.scale(
        geo["cases_sqrt"].min(),
        geo["cases_sqrt"].max()
    )


def make_style_function(colormap):
    def style(feature):
        value = feature["properties"]["cases_sqrt"]
        return {
            "fillColor": colormap(value) if value is not None else "transparent",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7,
        }
    return style


def create_map(geo: gpd.GeoDataFrame, colormap) -> folium.Map:
    m = folium.Map(
        location=[53.5511, 9.9937],
        zoom_start=11,
        tiles="cartodb positron"
    )

    style_function = make_style_function(colormap)

    folium.GeoJson(
        geo,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["name", "cases_display"],
            aliases=["Neighborhood:", "Cases:"]
        ),
    ).add_to(m)

    colormap.caption = "Crime cases"
    colormap.add_to(m)

    return m


def main():
    df_raw = extract_data_from_pdf(PDF_FILE, PDF_PAGES)
    df_clean = clean_data(df_raw)

    geo = prepare_geodata(df_clean, GEO_FILE)
    colormap = create_colormap(geo)

    m = create_map(geo, colormap)
    m.save("public/index.html")
    print("created map")


if __name__ == "__main__":
    main()
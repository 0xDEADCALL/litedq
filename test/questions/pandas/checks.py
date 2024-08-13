import json

from litedq import DataQuestions as dq


@dq.register("close_value_pd", "Check no invalid close values are present")
def check_close_value_pd(sales_pd):
    df = sales_pd.query(
        "(close_value < 0) or (deal_stage == 'Won' and close_value.isna())"
    )

    subject = json.dumps(df.to_dict(orient="records"))
    check_value = df.shape[0] == 0

    return subject, check_value


@dq.register("check_employees_pd", "Check each company has at least 10 employees")
def check_employees_pd(accounts_pd):
    df = accounts_pd.query("employees < 10")

    subject = json.dumps(df.to_dict(orient="records"))
    check_value = df.shape[0] == 0

    return subject, check_value


@dq.register(
    "check_product_pct_pd",
    "Check each product represents at least 10% of the total data asset",
)
def check_product_pd(sales_pd):
    df = (
        sales_pd.groupby(["product"])
        .agg(avail_cnt=("opportunity_id", "count"))
        .assign(avail_pct=lambda x: round(100 * x.avail_cnt / sales_pd.shape[0], 2))
        .reset_index()
    )

    subject = json.dumps(df.to_dict(orient="records"))
    check_pct = df.query("avail_pct < 10").shape[0] == 0

    return subject, check_pct

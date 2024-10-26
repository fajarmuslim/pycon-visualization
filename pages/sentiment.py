from utils.label import show_scorecard, select_df, chart_overtime
from text import df
LABEL = 'sentiment'

show_scorecard(label=LABEL, percentage=False)
show_scorecard(label=LABEL, percentage=True)
chart_overtime(label=LABEL)
select_df(df=df, label=LABEL)

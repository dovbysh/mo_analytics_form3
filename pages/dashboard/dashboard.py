from app import app
from pages.dashboard.dashboard_layout import make_dashboard_layout

import pages.dashboard.store_data_clbks
import pages.dashboard.slicers_clbks
import pages.dashboard.bar_chart_clbks
import pages.dashboard.datatable_clbks

layout = make_dashboard_layout()
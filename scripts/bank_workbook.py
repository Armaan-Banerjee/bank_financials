"""
Shared helpers for building "<BANK> FINANCIALS.xlsx" workbooks in banks/.

Standard structure: a "Cash Flow Statement" sheet (full statement, period
columns, most-recent-first) plus one sheet per Pillar 3 key metric (CET1
Capital, CET1 Ratio, Tier 1 Capital, Tier 1 Ratio, Total Capital, Total
Capital Ratio, Total RWAs, Leverage Ratio, LCR, NSFR, MREL Ratio). Each sheet
ends in a single merged, wrapped source-citation cell rather than a per-row
citation column.

Usage:
    from bank_workbook import BankWorkbook, PILLAR3_SHEET_NAMES

    wb = BankWorkbook(
        bank_name="Example Bank Plc",
        years=["FY2025", "FY2024", "FY2023"],
        header_color="0A2540",
    )
    wb.add_cash_flow_sheet(title=..., subtitle=..., rows=[...], sources_text=...)
    wb.add_metric_sheet("CET1 Capital", unit="£'000", rows_data=[...], sources_text=...)
    wb.add_long_form_sheet("Interim Pillar 3", headers=[...], rows=[...])
    ...
    wb.save("/Users/armaan/code/katalysis/banks/EXAMPLE BANK FINANCIALS.xlsx")

Row tuple formats:
    Cash flow `rows`: (kind, label, values) where kind is "SECTION" (label-only
        divider), "DATA" (a normal line item) or "TOTAL" (bolded subtotal/total).
        `values` is a dict of {year: number}; omit a year to leave it blank.
    Metric sheet `rows_data`: (label, values) pairs, values as above. Use
        string values (e.g. "82.94%", "Not publicly disclosed") freely -
        cells are written as-is.
"""

import re

import openpyxl
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

PILLAR3_SHEET_NAMES = [
    "CET1 Capital",
    "CET1 Ratio",
    "Tier 1 Capital",
    "Tier 1 Ratio",
    "Total Capital",
    "Total Capital Ratio",
    "Total RWAs",
    "Leverage Ratio",
    "LCR",
    "NSFR",
    "MREL Ratio",
]

_PERCENT_RE = re.compile(r"^\s*(-?[\d,]+\.?\d*)\s*%")


def _parse_percent(value):
    """Parse a displayed ratio value ("14.5%") into a float (14.5) for
    charting; returns None for non-numeric values ("Not disclosed", etc.)."""
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        m = _PERCENT_RE.match(value)
        if m:
            return float(m.group(1).replace(",", ""))
    return None


THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
SECTION_FONT = Font(bold=True)
TOTAL_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=13)
SUBTITLE_FONT = Font(italic=True, size=9, color="666666")
SOURCE_FONT = Font(italic=True, size=9, color="444444")


class BankWorkbook:
    def __init__(self, bank_name, years, year_label=None, header_color="0A2540"):
        """
        bank_name: used as the "<Bank Name> — <Sheet>" title on metric sheets.
        years: list of year keys (e.g. "FY2025"), most recent first - this
            order drives column order on every sheet.
        year_label: optional {year_key: column_header_text} override, e.g. to
            append entity/period flags like "FY2024*". Defaults to the key.
        header_color: hex fill color (no '#') for the header row - vary this
            per bank so workbooks are visually distinguishable.
        """
        self.bank_name = bank_name
        self.years = years
        self.year_label = year_label or {y: y for y in years}
        self.header_fill = PatternFill(
            start_color=header_color, end_color=header_color, fill_type="solid"
        )
        self.header_font = Font(color="FFFFFF", bold=True)
        self.wb = openpyxl.Workbook()
        self._first_sheet_used = False

    # -- internal styling helpers -------------------------------------------------
    def _style_header(self, ws, row, ncols):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=row, column=c)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.alignment = Alignment(
                horizontal="left", vertical="center", wrap_text=True
            )

    def _autosize(self, ws, widths):
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

    def _write_source_cell(self, ws, row, ncols, text, height=150):
        cell = ws.cell(row=row, column=1, value=text)
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
        cell.font = SOURCE_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
        ws.row_dimensions[row].height = height

    def _style_chart_axes(self, chart):
        # openpyxl's TextAxis/NumericAxis both default axPos to "l", which
        # puts the category axis on top of the value axis - fix the category
        # (x) axis onto the bottom and make sure both axes actually draw
        # their tick labels and lines.
        chart.x_axis.axPos = "b"
        chart.y_axis.axPos = "l"
        chart.x_axis.tickLblPos = "nextTo"
        chart.y_axis.tickLblPos = "nextTo"
        chart.x_axis.delete = False
        chart.y_axis.delete = False
        chart.x_axis.majorTickMark = "out"
        chart.y_axis.majorTickMark = "out"

    def _reserve_bottom_legend(self, chart, legend_h, plot_h, plot_top=0.12):
        # Pin the legend to its own band at the very bottom of the chart
        # area and explicitly shrink the plotting rectangle above it, so
        # Excel's automatic layout can't let a wrapped multi-line legend
        # encroach on the axis tick labels above it.
        chart.legend.layout = Layout(
            manualLayout=ManualLayout(
                xMode="edge", yMode="edge",
                x=0.02, y=1.0 - legend_h, h=legend_h, w=0.96,
            )
        )
        # ChartBase._write() overwrites plot_area.layout with chart.layout at
        # save time, so the plot rectangle must be set here, not on plot_area.
        chart.layout = Layout(
            manualLayout=ManualLayout(
                layoutTarget="inner",
                xMode="edge", yMode="edge",
                x=0.10, y=plot_top, w=0.85, h=plot_h,
            )
        )

    def _next_sheet(self, name):
        if not self._first_sheet_used:
            ws = self.wb.active
            ws.title = name[:31]
            self._first_sheet_used = True
            return ws
        return self.wb.create_sheet(title=name[:31])

    # -- public API -----------------------------------------------------------
    def add_cash_flow_sheet(
        self,
        title,
        subtitle,
        rows,
        sources_text,
        sheet_name="Cash Flow Statement",
        first_col_width=60,
        source_height=150,
        unit_suffix=" (£'000)",
    ):
        """
        rows: list of (kind, label, values) - kind in {"SECTION", "DATA", "TOTAL"}.
        """
        ws = self._next_sheet(sheet_name)
        ws.freeze_panes = "B4"
        ws["A1"] = title
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle
        ws["A2"].font = SUBTITLE_FONT

        ncols = 1 + len(self.years)
        headers = ["Line item"] + [
            f"{self.year_label[y]}{unit_suffix}" for y in self.years
        ]
        header_row = 3
        for c, h in enumerate(headers, start=1):
            ws.cell(row=header_row, column=c, value=h)
        self._style_header(ws, header_row, ncols)

        r = header_row + 1
        for kind, label, values in rows:
            ws.cell(row=r, column=1, value=label)
            if kind == "SECTION":
                ws.cell(row=r, column=1).font = SECTION_FONT
            else:
                for ci, y in enumerate(self.years, start=2):
                    ws.cell(row=r, column=ci, value=values.get(y))
                if kind == "TOTAL":
                    for c in range(1, ncols + 1):
                        ws.cell(row=r, column=c).font = TOTAL_FONT
            for c in range(1, ncols + 1):
                ws.cell(row=r, column=c).border = BORDER
            r += 1

        self._write_source_cell(ws, r + 1, ncols, sources_text, height=source_height)
        self._autosize(ws, [first_col_width] + [15] * len(self.years))
        return ws

    def add_metric_sheet(
        self,
        name,
        unit,
        rows_data,
        sources_text,
        note=None,
        first_col_width=46,
        source_height=150,
        note_height=60,
    ):
        """
        rows_data: list of (label, values) pairs, values a {year: value} dict
            (numbers or strings, e.g. "82.94%" / "Not publicly disclosed").
        """
        ws = self.wb.create_sheet(title=name[:31])
        ncols = 1 + len(self.years)
        ws["A1"] = f"{self.bank_name} — {name}"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = unit or ""
        ws["A2"].font = SUBTITLE_FONT

        headers = ["Metric"] + [self.year_label[y] for y in self.years]
        header_row = 3
        for c, h in enumerate(headers, start=1):
            ws.cell(row=header_row, column=c, value=h)
        self._style_header(ws, header_row, ncols)

        r = header_row + 1
        for label, values in rows_data:
            ws.cell(row=r, column=1, value=label)
            for ci, y in enumerate(self.years, start=2):
                ws.cell(row=r, column=ci, value=values.get(y))
            for c in range(1, ncols + 1):
                ws.cell(row=r, column=c).border = BORDER
            r += 1

        if note:
            ws.cell(row=r, column=1, value=f"Note: {note}").font = SUBTITLE_FONT
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
            ws.cell(row=r, column=1).alignment = Alignment(
                wrap_text=True, vertical="top"
            )
            ws.row_dimensions[r].height = note_height
            r += 1

        self._write_source_cell(ws, r + 1, ncols, sources_text, height=source_height)
        self._autosize(ws, [first_col_width] + [15] * len(self.years))
        return ws

    def add_long_form_sheet(
        self,
        name,
        headers,
        rows,
        title=None,
        subtitle=None,
        note=None,
        widths=None,
        hyperlink_cells=None,
        freeze_panes="A5",
    ):
        """Add an auxiliary long-form data sheet.

        This is intended for additional observations that do not fit the
        standard fixed annual columns, such as quarterly or semi-annual Pillar
        3 disclosures.

        ``headers`` is a list of column names and ``rows`` is a list of row
        lists/tuples with the same length.  ``hyperlink_cells`` is an optional
        mapping of ``(data_row_index, column_index)`` to URL, using zero-based
        indexes relative to the supplied data rows and headers.  ``widths`` is
        an optional list of column widths.
        """
        if not headers:
            raise ValueError("Long-form sheet requires at least one header")
        ncols = len(headers)
        for row in rows:
            if len(row) != ncols:
                raise ValueError(
                    f"Long-form row has {len(row)} values; expected {ncols}"
                )

        ws = self.wb.create_sheet(title=name[:31])
        ws["A1"] = title or f"{self.bank_name} — {name}"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle or ""
        ws["A2"].font = SUBTITLE_FONT

        header_row = 4
        for col, header in enumerate(headers, start=1):
            ws.cell(row=header_row, column=col, value=header)
        self._style_header(ws, header_row, ncols)

        hyperlink_cells = hyperlink_cells or {}
        for row_index, values in enumerate(rows):
            excel_row = header_row + 1 + row_index
            for col_index, value in enumerate(values):
                cell = ws.cell(row=excel_row, column=col_index + 1, value=value)
                cell.border = BORDER
                url = hyperlink_cells.get((row_index, col_index))
                if url:
                    cell.hyperlink = url
                    cell.style = "Hyperlink"

        if note:
            note_row = header_row + 1 + len(rows) + 1
            ws.cell(row=note_row, column=1, value=note)
            ws.merge_cells(
                start_row=note_row,
                start_column=1,
                end_row=note_row,
                end_column=ncols,
            )
            ws.cell(row=note_row, column=1).font = SOURCE_FONT
            ws.cell(row=note_row, column=1).alignment = Alignment(
                wrap_text=True, vertical="top", horizontal="left"
            )
            ws.row_dimensions[note_row].height = 60

        ws.freeze_panes = freeze_panes
        self._autosize(ws, widths or [18] * ncols)
        return ws

    def add_wide_interim_sheet(
        self,
        name,
        headers=None,
        rows=None,
        title=None,
        subtitle=None,
        note=None,
        widths=None,
        hyperlink_cells=None,
        freeze_panes="D5",
    ):
        """Add a wide interim Pillar 3 matrix from standard observation rows.

        ``rows`` uses the same eight-field records as ``add_long_form_sheet``:
        period, disclosure type, metric, value, unit, basis, source document,
        and page/table.  Periods become columns and metrics become rows.  Each
        populated value cell links to its source document; a compact source
        register below the matrix preserves disclosure type and page/table
        references.  ``hyperlink_cells`` may map the zero-based input row and
        source-document column (normally ``(row_index, 6)``) to a URL.  This
        keeps a readable source-document label in the workbook while using the
        official URL as the hyperlink target.
        """
        # Accept the existing long-form call shape as well as the simpler
        # ``rows=...`` form, so bank builders can be migrated mechanically.
        if rows is None:
            rows = headers
        if not rows:
            raise ValueError("Wide interim sheet requires at least one row")
        if any(len(row) != 8 for row in rows):
            raise ValueError("Wide interim rows must contain exactly 8 fields")

        periods = []
        metrics = []
        metric_meta = {}
        values = {}
        links = {}
        source_rows = []
        source_seen = set()
        hyperlink_cells = hyperlink_cells or {}
        for row_index, row in enumerate(rows):
            period, disclosure, metric, value, unit, basis, source, page = row
            if period not in periods:
                periods.append(period)
            if metric not in metrics:
                metrics.append(metric)
                metric_meta[metric] = (unit, basis)
            values[(metric, period)] = value
            # Only ever hyperlink a cell to a genuine URL. This used to fall
            # back to the plain source-document label text (e.g. "Q3 2022
            # Pillar 3 Supplement") whenever a build script didn't pass an
            # explicit URL for that row - openpyxl writes that text in
            # verbatim as `cell.hyperlink`, producing an invalid link Excel
            # either errors on or mistreats as a relative path, and it LOOKS
            # like a real citation (styled + clickable) even though it isn't
            # one. Leaving the cell as plain, unstyled text when no real URL
            # is available makes the gap visible instead of silently faking
            # a working citation - see IN-031.
            source_url = hyperlink_cells.get((row_index, 6))
            if source_url and not str(source_url).startswith(("http://", "https://")):
                source_url = None
            links[(metric, period)] = source_url
            source_key = (period, disclosure, source, page)
            if source_key not in source_seen:
                source_seen.add(source_key)
                source_rows.append((*source_key, source_url))

        ws = self.wb.create_sheet(title=name[:31])
        ws["A1"] = title or f"{self.bank_name} — {name}"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = subtitle or ""
        ws["A2"].font = SUBTITLE_FONT

        headers = ["Metric", "Unit", "Basis"] + periods
        header_row = 4
        for col, header in enumerate(headers, start=1):
            ws.cell(row=header_row, column=col, value=header)
        self._style_header(ws, header_row, len(headers))

        for row_index, metric in enumerate(metrics):
            excel_row = header_row + 1 + row_index
            unit, basis = metric_meta[metric]
            row_values = [metric, unit, basis]
            for col_index, value in enumerate(row_values, start=1):
                cell = ws.cell(row=excel_row, column=col_index, value=value)
                cell.border = BORDER
            for period_index, period in enumerate(periods, start=4):
                value = values.get((metric, period))
                cell = ws.cell(row=excel_row, column=period_index, value=value)
                cell.border = BORDER
                source = links.get((metric, period))
                if source and value not in (None, ""):
                    cell.hyperlink = source
                    cell.style = "Hyperlink"

        source_header_row = header_row + len(metrics) + 3
        ws.cell(row=source_header_row, column=1, value="Source register")
        ws.cell(row=source_header_row, column=1).font = SUBTITLE_FONT
        source_headers = ["Period", "Disclosure type", "Source document", "Page / table"]
        for col, header in enumerate(source_headers, start=1):
            ws.cell(row=source_header_row + 1, column=col, value=header)
        self._style_header(ws, source_header_row + 1, len(source_headers))
        for source_index, source_row in enumerate(source_rows):
            excel_row = source_header_row + 2 + source_index
            for col_index, value in enumerate(source_row[:4], start=1):
                cell = ws.cell(row=excel_row, column=col_index, value=value)
                cell.border = BORDER
                if col_index == 3 and source_row[4]:
                    cell.hyperlink = source_row[4]
                    cell.style = "Hyperlink"

        note_row = source_header_row + 2 + len(source_rows) + 1
        if note:
            ws.cell(row=note_row, column=1, value=f"Note: {note}")
            ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=len(headers))
            ws.cell(row=note_row, column=1).font = SOURCE_FONT
            ws.cell(row=note_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[note_row].height = 60

        ws.freeze_panes = freeze_panes
        self._autosize(ws, [32, 18, 34] + [15] * len(periods))
        return ws

    def add_overview_sheet(self, cash_flow_totals, cash_flow_unit, ratios, note=None):
        """
        Inserts an "Overview" sheet as the first tab: a summary table of
        headline cash flow totals and headline Pillar 3 ratios across all
        years, plus a clustered column chart (cash flow) and a line chart
        (ratios) - both rendered oldest-year-first left to right regardless
        of the most-recent-first column order used everywhere else.

        cash_flow_totals: list of (label, {year: number}) - e.g. net cash
            from operating/investing/financing activities, cash at year end.
            Pass an empty list ([]) for a Pillar-3-only workbook (e.g. an
            entity taking the FRS 101/102 cash-flow-statement exemption) -
            the cash-flow table/chart are then omitted entirely and only the
            ratios chart is built; see the "Cash Flow Statement" sheet for
            the exemption note in that case.
        cash_flow_unit: unit string for the table heading and chart axis,
            e.g. "£m" or "£'000". Ignored if cash_flow_totals is empty.
        ratios: list of (label, {year: value}) - values as displayed
            (e.g. "14.5%" or "Not publicly disclosed"); values that aren't
            a plain percentage are parsed as None and simply leave a gap
            in the chart rather than being plotted. Pass an empty list ([])
            for a bank with no disclosed Pillar 3 ratios at all - the ratios
            table/chart are then omitted entirely (fixed 2026-08-28; earlier
            build scripts worked around this by passing empty-{}-valued
            entries instead, e.g. build_caf_bank.py/build_brown_shipley.py -
            that workaround still works too, no need to change them).
        """
        ws = self.wb.create_sheet(title="Overview", index=0)
        ncols = 1 + len(self.years)
        headers = ["Line item"] + [self.year_label[y] for y in self.years]

        ws["A1"] = f"{self.bank_name} — Overview"
        ws["A1"].font = TITLE_FONT
        ws["A2"] = "Summary of cash flow and Pillar 3 disclosures across all years covered in this workbook"
        ws["A2"].font = SUBTITLE_FONT

        row = 4
        if cash_flow_totals:
            ws.cell(row=row, column=1, value=f"Cash Flow Summary ({cash_flow_unit})").font = SECTION_FONT
            row += 1
            cf_header_row = row
            for c, h in enumerate(headers, start=1):
                ws.cell(row=row, column=c, value=h)
            self._style_header(ws, row, ncols)
            row += 1
            cf_data_start = row
            for label, values in cash_flow_totals:
                ws.cell(row=row, column=1, value=label)
                for ci, y in enumerate(self.years, start=2):
                    ws.cell(row=row, column=ci, value=values.get(y))
                for c in range(1, ncols + 1):
                    ws.cell(row=row, column=c).font = TOTAL_FONT
                    ws.cell(row=row, column=c).border = BORDER
                row += 1
            cf_data_end = row - 1
        else:
            ws.cell(row=row, column=1,
                     value="Cash Flow Summary: not applicable — this entity does not publish a cash flow "
                           "statement (see the Cash Flow Statement sheet for the exemption basis).").font = SECTION_FONT
            row += 1
            cf_header_row = None

        row += 1
        if ratios:
            ws.cell(row=row, column=1, value="Pillar 3 Key Metrics").font = SECTION_FONT
            row += 1
            ratio_header_row = row
            for c, h in enumerate(headers, start=1):
                ws.cell(row=row, column=c, value=h)
            self._style_header(ws, row, ncols)
            row += 1
            for label, values in ratios:
                ws.cell(row=row, column=1, value=label)
                for ci, y in enumerate(self.years, start=2):
                    ws.cell(row=row, column=ci, value=values.get(y))
                for c in range(1, ncols + 1):
                    ws.cell(row=row, column=c).border = BORDER
                row += 1
            ratio_data_end = row - 1
        else:
            ws.cell(row=row, column=1,
                     value="Pillar 3 Key Metrics: not applicable — no ratios are disclosed for this "
                           "entity (see the individual Pillar 3 metric sheets).").font = SECTION_FONT
            row += 1
            ratio_header_row = None

        if note:
            row += 1
            ws.cell(row=row, column=1, value=f"Note: {note}").font = SUBTITLE_FONT
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
            ws.cell(row=row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[row].height = 45
            row += 1

        self._autosize(ws, [42] + [15] * len(self.years))

        # -- hidden numeric staging areas, oldest-year-first, for the two charts --
        # (built as separate chronological blocks rather than via a reversed
        # category axis, which flips the value axis to the wrong side in Excel)
        chrono_years = list(reversed(self.years))
        n_years = len(self.years)

        cf_stage_col = ncols + 3
        if cash_flow_totals:
            cf_stage_header_row = cf_header_row
            for ci, y in enumerate(chrono_years, start=1):
                ws.cell(row=cf_stage_header_row, column=cf_stage_col + ci, value=self.year_label[y])
            r = cf_stage_header_row + 1
            for label, values in cash_flow_totals:
                ws.cell(row=r, column=cf_stage_col, value=label)
                for ci, y in enumerate(chrono_years, start=1):
                    ws.cell(row=r, column=cf_stage_col + ci, value=values.get(y))
                r += 1
            cf_stage_end = r - 1

        ratio_stage_col = cf_stage_col + ncols + 2
        if ratios:
            ratio_stage_header_row = cf_header_row if cash_flow_totals else ratio_header_row
            for ci, y in enumerate(chrono_years, start=1):
                ws.cell(row=ratio_stage_header_row, column=ratio_stage_col + ci, value=self.year_label[y])
            r = ratio_stage_header_row + 1
            for label, values in ratios:
                ws.cell(row=r, column=ratio_stage_col, value=label)
                for ci, y in enumerate(chrono_years, start=1):
                    ws.cell(row=r, column=ratio_stage_col + ci, value=_parse_percent(values.get(y)))
                r += 1
            ratio_stage_end = r - 1

        for c in range(cf_stage_col, ratio_stage_col + ncols):
            ws.column_dimensions[get_column_letter(c)].hidden = True

        # -- charts --
        chart_row = row + 2
        if cash_flow_totals:
            bar = BarChart()
            bar.type = "col"
            bar.grouping = "clustered"
            bar.title = f"{self.bank_name} — Cash Flow Summary by Year"
            bar.y_axis.title = cash_flow_unit
            bar.height = 13
            bar.width = 24
            data = Reference(ws, min_col=cf_stage_col, max_col=cf_stage_col + n_years,
                              min_row=cf_stage_header_row + 1, max_row=cf_stage_end)
            bar.add_data(data, titles_from_data=True, from_rows=True)
            cats = Reference(ws, min_col=cf_stage_col + 1, max_col=cf_stage_col + n_years,
                              min_row=cf_stage_header_row, max_row=cf_stage_header_row)
            bar.set_categories(cats)
            bar.visible_cells_only = False  # source data lives in hidden staging columns
            self._style_chart_axes(bar)
            bar.legend.position = "b"
            self._reserve_bottom_legend(bar, legend_h=0.16, plot_h=0.55, plot_top=0.14)
            ws.add_chart(bar, f"A{chart_row}")
            line_chart_row = chart_row + 22
        else:
            line_chart_row = chart_row

        if not ratios:
            return ws

        line = LineChart()
        line.title = f"{self.bank_name} — Pillar 3 Key Metrics by Year"
        line.y_axis.title = "%"
        line.height = 16
        line.width = 24
        ldata = Reference(ws, min_col=ratio_stage_col, max_col=ratio_stage_col + n_years,
                           min_row=ratio_stage_header_row + 1, max_row=ratio_stage_end)
        line.add_data(ldata, titles_from_data=True, from_rows=True)
        lcats = Reference(ws, min_col=ratio_stage_col + 1, max_col=ratio_stage_col + n_years,
                           min_row=ratio_stage_header_row, max_row=ratio_stage_header_row)
        line.set_categories(lcats)
        line.visible_cells_only = False  # source data lives in hidden staging columns
        self._style_chart_axes(line)
        line.legend.position = "b"
        self._reserve_bottom_legend(line, legend_h=0.22, plot_h=0.50, plot_top=0.12)
        for s in line.series:
            s.smooth = False
        ws.add_chart(line, f"A{line_chart_row}")

        return ws

    def add_not_disclosed_metric_sheets(self, names, sources_text, per_note=None):
        """Convenience for the common "no Pillar 3 doc exists" case - fills a
        list of metric sheets with a single "Not publicly disclosed" row each.
        per_note: optional {name: note_text} for sheet-specific notes."""
        per_note = per_note or {}
        for name in names:
            self.add_metric_sheet(
                name,
                None,
                [(name, {y: "Not publicly disclosed" for y in self.years})],
                sources_text,
                note=per_note.get(name),
            )

    def save(self, path):
        self.wb.save(path)
        print("Saved workbook with sheets:", self.wb.sheetnames)
        return path

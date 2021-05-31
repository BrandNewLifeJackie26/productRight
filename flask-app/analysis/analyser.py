import pandas as pd


"""
    Analyser: provides functions to analyze pandas.DataFrame and output stats about them
"""


class Analyser:
    def __init__(self) -> None:
        pass

    '''Helpers'''

    def generate_base_counts(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).count().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).count().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]

    def generate_base_sum(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).sum().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).sum().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]

    def conversions(self, data, grouped, metric, comp, subset=(), choice=()):
        if subset != ():
            nov_grouped = data.loc[data[subset] == choice]
            nov_grouped = nov_grouped.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]
        else:
            nov_grouped = data.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped = nov_grouped.pivot(
            index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped['v2c: views to cart'] = (nov_grouped.cart/nov_grouped.view)
        nov_grouped['c2p: cart to payment'] = (
            nov_grouped.purchase/nov_grouped.cart)
        nov_grouped['v2p: views to payment'] = (
            nov_grouped.purchase/nov_grouped.view)
        nov_grouped = nov_grouped.loc[nov_grouped[grouped].isin(
            list(comp[grouped].unique()))]
        nov_grouped_t = nov_grouped.T.loc[[
            grouped, 'v2c: views to cart', 'c2p: cart to payment', 'v2p: views to payment']]
        nov_grouped_t.columns = nov_grouped_t.loc[grouped, :]
        nov_grouped_t = nov_grouped_t.drop(grouped)
        nov_grouped_t.reset_index(inplace=True)
        nov_grouped_t = nov_grouped_t.melt(id_vars=['event_type'],
                                           var_name=grouped,
                                           value_name="conversion_value")
        return nov_grouped_t

    def funnel(self, data, grouped, metric, subset=(), choice=()):
        if subset != ():
            nov_grouped = data.loc[data[subset] == choice]
            nov_grouped = nov_grouped.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]
        else:
            nov_grouped = data.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped = nov_grouped.pivot(
            index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped = nov_grouped.dropna().T
        nov_grouped.columns = nov_grouped.loc[grouped, :]
        nov_grouped = nov_grouped.drop(grouped)
        nov_grouped.reset_index(inplace=True)
        nov_grouped = nov_grouped.melt(id_vars=['event_type'],
                                       var_name=grouped,
                                       value_name="funnel_value")
        return nov_grouped

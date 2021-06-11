import pandas as pd


class Analyser:
    '''
    Analyser class provides functions to analyze pandas.DataFrame and output the graphs
    '''
    def __init__(self) -> None:
        pass

    '''Helpers'''

    def generate_base_counts(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        '''
        This function groups the data by the column specified in grouped and generates the total number (counts) of
        filtered by the given metric

        :param data: input dataframe
        :param metrics: metrics of which the counts are generated. For eg: Price
        :param grouped: condition to be used for grouping. For eg: brand
        :param top: Number of data entries to be returned
        :param asc: bool to represent sort the return dataframe in ascending order. Used for top vs bottom set
        :param subset: if you want the dataset to be further subsetted by a value. For eg: you want top brands for a specific category
                        you would provide "brand". This is an option input.
        :param choice: If subset is provided, choice allows you to select which value in the subset you want to filter the data on
        :return: data frame representing the data filtered by the options provided
        :rtype: pandas Dataframe
        '''
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).count().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).count().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]

    def generate_base_sum(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        '''
        This function groups the data by the column specified in grouped and generates the sum of the value.
        This function is used to generate the sum of price, or total revenue

        :param data: input dataframe
        :param metrics: metrics of which the counts are generated. For eg: Price
        :param grouped: condition to be used for grouping. For eg: brand
        :param top: Number of data entries to be returned
        :param asc: bool to represent sort the return dataframe in ascending order. Used for top vs bottom set
        :param subset: if you want the dataset to be further subsetted by a value. For eg: you want top brands for a specific category
                        you would provide "brand". This is an option input.
        :param choice: If subset is provided, choice allows you to select which value in the subset you want to filter the data on
        :return: data frame representing the data filtered by the options provided
        :rtype: pandas Dataframe
        '''
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).sum().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).sum().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]

    def conversions(self, data, grouped, metric, comp, subset=(), choice=()):
        '''
        This function groups the data by the column specified in grouped and generates the conversions for the given condtions.
        There are 3 conversions provided:
            1) v2c(viewed to cart): count of all carts/ count of all views
            2) c2p(cart to purchase): count of all purchases/count of all carts
            3) v2p(view to purchase): count of all purchases/count of all views

        :param data: input dataframe
        :param metrics: metrics of which the counts are generated for performing the division for conversions. Input is usually user_session
        :param grouped: condition to be used for grouping. For eg: brand (if you want conversion by brand)
        :param top: Number of data entries to be returned
        :param asc: bool to represent sort the return dataframe in ascending order. Used for top vs bottom set
        :param subset: if you want the dataset to be further subsetted by a value. For eg: you want top brands for a specific category
                        you would provide "brand". This is an option input.
        :param choice: If subset is provided, choice allows you to select which value in the subset you want to filter the data on
        :return: data frame representing the data filtered by the options provided
        :rtype: pandas Dataframe
        '''

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
        '''
        This function groups the data by the column specified in grouped and generates the funnel for the given condtions.
        There are 3 stages in the funnel provided:
            1) views: number of user sessions in view stage
            2) carts: number of user sessions in cart stage
            3) purchases: number of user sessions in purchase stage

        :param data: input dataframe
        :param metrics: metrics of which the counts are generated. Input is usually user_session
        :param grouped: condition to be used for grouping. For eg: brand (if you want funnel by brand)
        :param top: Number of data entries to be returned
        :param asc: bool to represent sort the return dataframe in ascending order. Used for top vs bottom set
        :param subset: if you want the dataset to be further subsetted by a value. For eg: you want top brands for a specific category
                        you would provide "brand". This is an option input.
        :param choice: If subset is provided, choice allows you to select which value in the subset you want to filter the data on
        :return: data frame representing the data filtered by the options provided
        :rtype: pandas Dataframe
        '''

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

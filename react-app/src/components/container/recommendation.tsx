import styles from './recommendation.css';
import { useState, useEffect } from 'react';
import { Cascader, Table, Button } from 'antd';

export default function Recommendation() {
    // Item selecter
    // TODO: Get item id from back end
    const [itemId, setItemId] = useState('');
    const [item, setItem] = useState({}); // Item information of current selected item
    const options = [
      {
        value: '1003461',
        label: '1003461',
      },
      {
        value: '2700588',
        label: '2700588',
      },
    ];

    function itemIdOnChange(value) {
      setItemId(value[0]);
    };

    // Recommendation data from back end (table-like json)
    const [nearestItemsDataSource, setNearestItemsDataSource] = useState([]);
    const [nearestUsersDataSource, setNearestUsersDataSource] = useState([]);
    const [nearestItemsColumns, setNearestItemsColumns] = useState([]);
    const [nearestUsersColumns, setNearestUsersColumns] = useState([]);
    
    // Get table-like json from back-end
    useEffect(()=>{
      if (itemId === '' || itemId === undefined) {
        setItem({});
        return;
      }

      fetch(`/api/get-item/${itemId}`).then(res => res.json()).then(data => {
        setItem(data);
      })

      fetch(`/api/nearest-items/${itemId}`).then(res => res.json()).then(data => {
        // Convert table-like json data to antd Table data
        let ds = [];
        for (const key in data) {
          let newObject = {
            ...data[key],
            key: key,
          };
          ds.push(newObject);
        }
        setNearestItemsDataSource(ds);

        // Extract column names for antd Table columns
        // TODO: if there is no entry in data
        let cols = [];
        for (const attribute in data[0]) {
          let newObject = {
            key: attribute,
            dataIndex: attribute,
            title: attribute,
          };
          cols.push(newObject);
        }
        setNearestItemsColumns(cols);
      });

      fetch(`/api/nearest-users-from-item/${itemId}`).then(res => res.json()).then(data => {
        // Convert table-like json data to antd Table data
        let ds = [];
        for (const key in data) {
          let newObject = {
            ...data[key],
            key: key,
          };
          ds.push(newObject);
        }
        setNearestUsersDataSource(ds);

        // Extract column names for antd Table columns
        // TODO: if there is no entry in data
        let cols = [];
        for (const attribute in data[0]) {
          let newObject = {
            key: attribute,
            dataIndex: attribute,
            title: attribute,
          };
          cols.push(newObject);
        }
        setNearestUsersColumns(cols);
      });
    }, [itemId]);

    return (
        <div>
            <h1 className={styles.title}>Recommendation</h1>
            <table width='100%'>
              <tbody>
                <tr>
                  <td rowSpan={2} width='20%'>
                    <Cascader 
                      options={options}
                      onChange={itemIdOnChange}
                      placeholder="Please select the item id you want to analyze"
                    />
                  </td>

                  <td width='80%'>
                    <Table 
                      dataSource={nearestItemsDataSource}
                      columns={nearestItemsColumns}
                      title={() => {
                        return (
                          <table>
                            <tbody>
                              <td>Nearest items for item_id:<Button type='primary'>{itemId}</Button></td>
                              <td>category:<Button type='dashed'>{item['category_code']}</Button></td>
                              <td>brand:<Button type='dashed'>{item['brand']}</Button></td>
                            </tbody>
                          </table>
                        )}}
                      scroll={{ y: 240 }}
                    />
                  </td>
                </tr>
                
                <tr>
                  <td width='80%'>
                    <Table 
                      dataSource={nearestUsersDataSource}
                      columns={nearestUsersColumns}
                      title={() => {
                        return (
                          <table>
                            <tbody>
                              <td>Nearest users for item_id:<Button type='primary'>{itemId}</Button></td>
                              <td>category:<Button type='dashed'>{item['category_code']}</Button></td>
                              <td>brand:<Button type='dashed'>{item['brand']}</Button></td>
                            </tbody>
                          </table>
                        )}}
                      scroll={{ y: 240 }}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
        </div>
    );
}
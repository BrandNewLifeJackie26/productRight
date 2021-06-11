import styles from './recommendation.css';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { useState, useEffect } from 'react';
import { Tooltip, Form, InputNumber, Table, Button } from 'antd';

export default function Recommendation() {
    // Item selecter
    // TODO: Get item id from back end
    const [itemId, setItemId] = useState('');
    const [item, setItem] = useState({}); // Item information of current selected item

    function itemIdOnChange(values) {
      setItemId(values['itemId']);
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
        <div className={styles.recommendation}>
          <div className={styles.recommInput}>
            <Form layout="inline" onFinish={itemIdOnChange}>
              <Form.Item
                label="Item ID"
                name="itemId"
                rules={[{ required: true, message: "Incorrect item ID!" }]}
                labelCol={{ span: 12 }}
              >
                <InputNumber style={{ width: "120px" }}/>
              </Form.Item>

              <Form.Item
                wrapperCol= {{ span: 8 }}
              >
                <Button type="primary" htmlType="submit">Recommend</Button>
              </Form.Item>
            </Form>
          </div>

          <div className={styles.recommResult}>
            <div>
              <Table 
                dataSource={nearestItemsDataSource}
                columns={nearestItemsColumns}
                title={() => {
                  return (
                    <table>
                      <tbody>
                        <td>
                          <Tooltip title={"Provides list of similar items to the input item"}>
                            <QuestionCircleOutlined/>
                          </Tooltip>
                        </td>
                        <td>Nearest items for item_id:<Button type='primary' className={styles.itemAttributeButton}>{itemId}</Button></td>
                        <td>category:<Button type='dashed' className={styles.itemAttributeButton}>{item['category_code']}</Button></td>
                        <td>brand:<Button type='dashed' className={styles.itemAttributeButton}>{item['brand']}</Button></td>
                      </tbody>
                    </table>
                  )}}
                scroll={{ y: 240 }}
                style={{ marginBottom: "10%" }}
              />
            </div>
                  
            <div>
              <Table 
                dataSource={nearestUsersDataSource}
                columns={nearestUsersColumns}
                title={() => {
                  return (
                    <table>
                      <tbody>
                      <td>
                          <Tooltip title={"Provides list of potential buyers for the input item"}>
                            <QuestionCircleOutlined/>
                          </Tooltip>
                        </td>
                        <td>Nearest users for item_id:<Button type='primary' className={styles.itemAttributeButton}>{itemId}</Button></td>
                        <td>category:<Button type='dashed' className={styles.itemAttributeButton}>{item['category_code']}</Button></td>
                        <td>brand:<Button type='dashed' className={styles.itemAttributeButton}>{item['brand']}</Button></td>
                      </tbody>
                    </table>
                  )}}
                scroll={{ y: 240 }}
              />
            </div>
          </div>
          
        </div>
    );
}
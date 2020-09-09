import React from 'react';
import { Link } from '@reach/router';
import { View } from '@/Types';
import Banner from '@/Components/Banner';
import '@/css/Shipments.css';


const Shipments: React.FC<View> = () => {
  return (
    <div className="Shipments view col-10 col-sm-12 col-mx-auto">
      <Banner>
        <ul className="breadcrumb">
          <li className="breadcrumb-item">Home</li>
          <li className="breadcrumb-item">
            <Link to="/">shipments</Link>
          </li>
        </ul>
      </Banner>

      <div className="card column col-12">

        <table className="table table-striped table-hover text-small">
          <thead>
            <tr>
              <th>shipment</th>
              <th>carrier</th>
              <th>shipper</th>
              <th>recipient</th>
              <th>delivery</th>
              <th>price</th>
              <th>status</th>
            </tr>
          </thead>
          <tbody>
            <tr className="active">
              <td>230498309434</td>
              <td>DHL</td>
              <td>
                <span>PSP Tech</span><br/>
                <span>Montreal, CA</span>
              </td>
              <td>
                <span>SM Headquater</span><br/>
                <span>Halifax, CA</span>
              </td>
              <td>
                <span>Expected On</span><br/>
                <span>Tues, 20 August</span>
              </td>
              <td>$45.00</td>
              <td>IN-TRANSIT</td>
            </tr>
            <tr>
              <td>230498309434</td>
              <td>DHL</td>
              <td>
                <span>PSP Tech</span><br/>
                <span>Montreal, CA</span>
              </td>
              <td>
                <span>SM Headquater</span><br/>
                <span>Halifax, CA</span>
              </td>
              <td>
                <span>Expected On</span><br/>
                <span>Tues, 20 August</span>
              </td>
              <td>$45.00</td>
              <td>IN-TRANSIT</td>
            </tr>
            <tr className="active">
              <td>230498309434</td>
              <td>DHL</td>
              <td>
                <span>PSP Tech</span><br/>
                <span>Montreal, CA</span>
              </td>
              <td>
                <span>SM Headquater</span><br/>
                <span>Halifax, CA</span>
              </td>
              <td>
                <span>Expected On</span><br/>
                <span>Tues, 20 August</span>
              </td>
              <td>$45.00</td>
              <td>IN-TRANSIT</td>
            </tr>
          </tbody>
        </table>

        <div className="card-footer">
          <ul className="pagination">
            <li className="page-item disabled">
              <a href="#" tabIndex={-1}>Previous</a>
            </li>
            <li className="page-item active">
              <a href="#">1</a>
            </li>
            <li className="page-item">
              <a href="#">2</a>
            </li>
            <li className="page-item">
              <a href="#">3</a>
            </li>
            <li className="page-item">
              <span>...</span>
            </li>
            <li className="page-item">
              <a href="#">12</a>
            </li>
            <li className="page-item">
              <a href="#">Next</a>
            </li>
          </ul>
        </div>
      </div>

    </div>
  );
}

export default Shipments;
import React, {useState, useEffect} from "react";
import axios from "axios";
import Table from 'react-bootstrap/Table';
import ReactPaginate from "react-paginate";
import IdentityComponent from "../IdentityComponent/IdentityComponent";




const ScanComponent = () => {
    var limit = 20;
    const [scan, setScan] = useState([]);
    const [count, setCount] = useState(0);
    
    useEffect(() => {
        axios.get("http://127.0.0.1:8081/api/scan/get/?limit=" + limit)
        .then(res => {
            setScan(res.data.results);
            setCount(res.data.count);
        })
        .catch(err => {
            console.log(err);
        });
    }, []);

    const fetchScans = (currentPage) => {
        axios.get("http://127.0.0.1:8081/api/scan/get/?limit=" + limit + "&offset=" + (currentPage-1)*limit)
        .then(res => {
            setScan(res.data.results);
        })
        .catch(err => {
            console.log(err);
        });
    }

    const handlePageClick = (data) => {
        let currentPage = data.selected + 1;
        fetchScans(currentPage);
    }
     
    return (
        <div className="container">
            <h1>Scan</h1>
            <ReactPaginate
                    previousLabel={"previous"}
                    nextLabel={"next"}
                    breakLabel={"..."}
                    breakClassName={"break-me"}
                    pageCount={Math.ceil(count / limit)}
                    marginPagesDisplayed={0}
                    pageRangeDisplayed={3}
                    onPageChange={handlePageClick}
                    containerClassName={"pagination"}
                    subContainerClassName={"pages pagination"}
                    activeClassName={"active"}
                    pageClassName={"page-item"}
                    pageLinkClassName={"page-link"}
                    previousLinkClassName={"page-link"}
                    nextLinkClassName={"page-link"}
                />
            <div className="main_table">
                <Table striped bordered hover>
                    <thead>
                        <tr>
                        <th>User ID</th>
                        <th>Flags</th>
                        <th>Verdict Type</th>
                        <th>Verdict Result</th>
                        <th>Verdict Name</th>
                        <th>Verdict Value</th>
                        <th>Identity</th>
                        </tr>
                    </thead>
                    <tbody>
                        {scan.map((scan) => (
                            <tr key={scan.id}>
                                <td>{scan.user_id}</td>
                                <td>{scan.flags}</td>
                                <td>{scan.verdict_type}</td>
                                <td>{scan.verdict_result}</td>
                                <td>{scan.verdict_name}</td>
                                <td>{scan.verdict_value}</td>
                                <td><IdentityComponent identity_id={scan.identity} /></td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </div>
        </div>
    );
};

export default ScanComponent;



import { useDispatch, useSelector } from "react-redux";
import {
  MDBPagination,
  MDBPaginationItem,
  MDBPaginationLink,
} from "mdb-react-ui-kit";
import { searchPackage } from "../store/actions/searchActions";

const Pagination = ({ currentPage, totalPages }) => {
  const query = useSelector((state) => state.search.query);

  const maxVisibleItems = 5;
  let startPage = Math.max(currentPage - Math.floor(maxVisibleItems / 2), 1);
  let endPage = Math.min(startPage + maxVisibleItems - 1, totalPages);
  const dispatch = useDispatch();

  const handlePageChange = (page) => {
    dispatch(searchPackage(query, page));
  };

  return (
    <nav aria-label="...">
      <MDBPagination className="mb-0">
        <MDBPaginationItem
          disabled={currentPage + 1 === 1}
          onClick={() => handlePageChange(currentPage - 1)}
        >
          <MDBPaginationLink aria-disabled="true">Previous</MDBPaginationLink>
        </MDBPaginationItem>
        {Array.from(
          { length: endPage - startPage + 1 },
          (_, i) => i + startPage
        ).map((page) => (
          <MDBPaginationItem
            key={page}
            active={currentPage + 1 === page}
            onClick={() => handlePageChange(page - 1)}
          >
            <MDBPaginationLink>{page}</MDBPaginationLink>
          </MDBPaginationItem>
        ))}
        <MDBPaginationItem
          disabled={currentPage + 1 === totalPages}
          onClick={() => handlePageChange(currentPage + 1)}
        >
          <MDBPaginationLink>Next</MDBPaginationLink>
        </MDBPaginationItem>
      </MDBPagination>
    </nav>
  );
};

export default Pagination;

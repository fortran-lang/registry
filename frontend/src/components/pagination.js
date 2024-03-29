import { useDispatch, useSelector } from "react-redux";
import {
  MDBPagination,
  MDBPaginationItem,
  MDBPaginationLink,
} from "mdb-react-ui-kit";
import { searchPackage } from "../store/actions/searchActions";

const Pagination = ({ currentPage, totalPages }) => {
  const dispatch = useDispatch();
  const query = useSelector((state) => state.search.query);
  const orderBy = useSelector((state) => state.search.orderBy);

  const maxVisibleItems = 5;
  const startPage = Math.max(currentPage - Math.floor(maxVisibleItems / 2), 1);
  const endPage = Math.min(startPage + maxVisibleItems - 1, totalPages);

  const handlePageChange = (page) => {
    dispatch(searchPackage(query, page, orderBy));
  };

  const generatePageTiles = () => {
    return Array.from(
      { length: endPage - startPage + 1 },
      (_, i) => i + startPage
    );
  };

  return (
    <nav aria-label="Pagination">
      <MDBPagination className="mb-0">
        <MDBPaginationItem
          disabled={currentPage + 1 === 1}
          onClick={() => handlePageChange(currentPage - 1)}
        >
          <MDBPaginationLink aria-disabled="true">Previous</MDBPaginationLink>
        </MDBPaginationItem>
        {generatePageTiles().map((page) => (
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

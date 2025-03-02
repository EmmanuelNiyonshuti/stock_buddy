"""This module provides a reusable function to paginate SQLAlchemy query results, 
ensuring efficient data retrieval and structured API responses.
"""
def paginate_query(query, page, per_page):
    """
    General utility function for paginating query results.
    :param query: SQLAlchemy query object
    :param page: Requested page number
    :param per_page: Number of items per page
    :return: Dict containing paginated results and metadata
    """
    paginated_data: Pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": [item.to_dict() for item in paginated_data.items],
        "total_items": paginated_data.total,
        "total_pages": paginated_data.pages,
        "current_page": paginated_data.page,
        "per_page": paginated_data.per_page,
        "has_next": paginated_data.has_next,
        "has_prev": paginated_data.has_prev,
    }

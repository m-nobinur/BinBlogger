# generates tags
def gen_tags(post_list, num=3):
    """this function will generate variable number of tags from the given

    Args:
        post_list (list): a list of post object
        num (int, optional): amount of tags to generate. Defaults to 3.

    Returns:
        list: num amount of tags (Defaults 3)
    """
    all_tag_list = [post.tags.split(',') for post in post_list]
    tags = set([tag.strip() for tags in all_tag_list for tag in tags])

    return list(tags)[:num]


# generates top categories
def gen_top_categories(cat_list, num: int = 3):
    """this function is responsible to generate variable number top categories 

    Args:
        cat_list (list): categories from those top will be calculated
        num (int): total number of top categories

    Returns:
        list: A list of top categories
    """

    top_categories = []
    top_categories = sorted(cat_list, key=lambda x: len(
        x.post_set.all()), reverse=True)[:num]

    return top_categories

def rating_average(rating_list):
	if not rating_list:
		return 0
	return sum(rating_list)/len(rating_list)


def set_filename_lower(filename):
	return filename.lower()

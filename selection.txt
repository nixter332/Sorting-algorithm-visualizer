def selection_sort(draw_info, ascending=True):
		lst=draw_info.lst

		if ascending:
			for i in range(len(lst)):
				min_idx = i
				for j in range(i+1, len(lst)):
					if lst[min_idx] > lst[j]:
						min_idx = j
				num1=lst[i]
				num2=lst[min_idx]
				lst[i], lst[min_idx] = lst[min_idx], lst[i]
				draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
				yield True
		else:
			for i in range(len(lst)):
				max_idx = i
				for j in range(i+1, len(lst)):
					if lst[max_idx] < lst[j]:
						max_idx = j
				num1=lst[i]
				num2=lst[max_idx]
				lst[i], lst[max_idx] = lst[max_idx], lst[i]
				draw_list(draw_info, {i: draw_info.GREEN, max_idx: draw_info.RED}, True)
				yield True

		return lst
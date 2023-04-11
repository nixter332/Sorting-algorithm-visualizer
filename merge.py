def merge_sort(draw_info, ascending = True):
    lst = draw_info.lst
    width = 1
    n = len(lst)
    while (width < n):
        l=0
        
        while (l < n):
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1) 
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            merge(lst, l, m, r, ascending)
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            l += width * 2
        width *= 2
        
    return lst

def merge(lst, l, m, r, ascending = True):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    
    for i in range(0, n1):
        L[i] = lst[l + i]
        
    for i in range(0, n2):
        R[i] = lst[m + i + 1]
        
    i, j, k = 0, 0, l
    
    if ascending:
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1
    
        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1
    
        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1
    else:
        while i < n1 and j < n2:
            if L[i] >= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1
    
        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1
    
        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1
	    
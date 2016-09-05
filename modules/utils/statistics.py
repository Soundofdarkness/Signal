import resource


def get_heap_size():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage

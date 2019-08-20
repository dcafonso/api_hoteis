def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5,
                          diaria_min=0, diaria_max=99999, limit=50, offset=0, **dados):
    if cidade:
        return {
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "cidade": cidade,
            "limit": limit,
            "offset": offset,
        }
    return {
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset,
    }


def select(com_cidade=False):
    if com_cidade:
        return "SELECT * FROM hoteis\
                WHERE (estrelas >= ? AND estrelas <= ?)\
                 AND (diaria >= ? AND diaria <= ?)\
                 AND cidade = ?\
                 LIMIT ? OFFSET ?"
    else:
        return "SELECT * FROM hoteis\
                WHERE (estrelas >= ? AND estrelas <= ?)\
                 AND (diaria >= ? AND diaria <= ?)\
                 LIMIT ? OFFSET ?"

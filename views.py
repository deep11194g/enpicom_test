from flask import request
import db


def add_dna():
    try:
        dna_sequence_string = request.form['sequence_string']
    except KeyError:
        response_body = {
            'code': 'BAD REQUEST',
            'message': 'Request Payload must have key `sequence_string`'
        }
        status_code = 400
        return response_body, status_code

    allowed_chars = list('ATGC')
    for nucleotide in dna_sequence_string:
        if nucleotide not in allowed_chars:
            response_body = {
                'code': 'BAD REQUEST',
                'message': 'DNA Sequence string can only have A/T/G/C`'
            }
            status_code = 400
            return response_body, status_code

    dna_id = db.insert_dna(sequence=dna_sequence_string)
    response_body = {
        'data': {
            'id': dna_id,
            'sequence_string': dna_sequence_string
        }
    }
    status_code = 200
    return response_body, status_code


def find_matching_dnas():
    try:
        search_text = request.args['search']
    except KeyError:
        response_body = {
            'code': 'BAD REQUEST',
            'message': 'Query Param `search` text field is required'
        }
        status_code = 400
        return response_body, status_code
    try:
        lev_score_threshold = int(request.args.get('threshold', 0))
    except TypeError:
        response_body = {
            'code': 'BAD REQUEST',
            'message': 'Query Param `threshold` must be of type integer'
        }
        status_code = 400
        return response_body, status_code

    response_body = {
        'data': db.fetch_dna(search_text, lev_score_threshold)
    }
    status_code = 200
    return response_body, status_code

import json
import logging
import re
import sys
from datetime import date, datetime

import pymysql
import rds_config

#rds settings
rds_host  = rds_config.host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(
        rds_host,
        user=name,
        passwd=password,
        db=db_name,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor
    )
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()


def format_object_datetimes(obj):
    for k,v in obj.items():
        logger.info(type(v))
        if type(v) == datetime:
            obj[k] = v.strftime("%Y-%m-%DT%H:%M:%SZ")


class DBTool():
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def get_engine_ticket(self, *args, **kwargs):
        query = """
        SELECT * FROM Tickets
        WHERE ticketSourceId = %s
        AND externalId = %s
        LIMIT 1
        """

        query_args = (kwargs["ticketSourceId"], kwargs["externalId"])
        self.cur.execute(query, query_args)
        ticket = self.cur.fetchone()

        format_object_datetimes(ticket)

        return ticket


logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def json_response(data):
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    with conn.cursor() as cur:
        dbtool = DBTool(conn, cur)
        resp = getattr(dbtool, event["fn"])(*event["args"], **event["kwargs"])

    logger.info(resp)

    return resp

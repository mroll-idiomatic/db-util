var DBTOOL_URL = "CHANGEME";


function executeQuery(query) {
  var options = {
    'method': 'post',
    'headers': {
      'x-api-key': 'CHANGEME',
    },
    'contentType': 'application/json',
    'payload': JSON.stringify(query.params)
  };
  var response = UrlFetchApp.fetch(DBTOOL_URL, options);
  
  var json = response.getContentText();
  var data = JSON.parse(json);
  
  return data;
}

function GetEngineTicket(id) {
  var idParamName = typeof id === 'string' ? "externalId" : "id";
  var query = {
    params: {
      fn: "get_engine_ticket",
      kwargs: {
        ticketSourceId: 100
      },
      args: []
    }
  }
  query.params.kwargs[idParamName] = id;
  Logger.log(query);
  
  var results = executeQuery(query);
  var header = Object.keys(results);
  var fields = header.map(function(colname) { return "" + results[colname]; })
  
  return [header].concat([fields]);
}

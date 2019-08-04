#mitmdump -r out.flows -n --set flow_detail=0 -s purchases.py

from mitmproxy import ctx
import json
import csv
from datetime import datetime

class iTunesPurchaseExport:
	def __init__(self):
		self.purchases = {}

	def response(self, flow):
		#if "png" not in flow.request.path:
		#	print(flow.request.path)
		if 'purchases?' in flow.request.path:
			decoded = json.loads(flow.response.content.decode(encoding="utf-8"))
			for day in decoded["data"]["attributes"]["purchases"]:
				for item in day["items"]:
					if "Movie Rental" in item["kind"]:
						print(item["item-name"])
						list_item = {"item-name" : item["item-name"], "item-id" : item["item-id"], "item-price" : item["price"], "purchase-date" : item["purchase-date"] }
						#self.purchases.append(list_item)
						date_object = datetime.strptime(list_item["purchase-date"], "%d %b %Y")
						self.purchases.update( { int(date_object.strftime('%Y%m%d') + item["item-id"]) : list_item } )

	def done(self):
		with open("/Users/username/Desktop/itunes_output.csv", 'w') as f:
			w = csv.writer(f)
			w.writerow(self.purchases[list(self.purchases.keys())[0]].keys())
			for list_item in self.purchases:
				w.writerow(self.purchases[list_item].values())

addons = [
    iTunesPurchaseExport()
]

# main_app.py
from flask import Flask
from flask_restful import Api
from resources.policy_resource import PolicyResource
from resources.placeholder_resource import PlaceholderResource
from resources.claim_resource import ClaimResource
from resources.delete_policy_resource import DeletePolicyResource
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
api = Api(app)
metrics = PrometheusMetrics(app)

@app.route('/metrics')
def metrics():
    return metrics.export()

# Register resources
api.add_resource(PolicyResource, '/api/policy') 
api.add_resource(PlaceholderResource, '/api/policyholder', '/api/policyholder/<string:name>')
api.add_resource(ClaimResource, '/api/claim/<string:name>')
api.add_resource(DeletePolicyResource, '/api/delete_policy')
@app.route('/'  )
def index():
    return "Welcome to the Insurance Policy Management System API"

if __name__ == '__main__':
    app.run(debug=True)

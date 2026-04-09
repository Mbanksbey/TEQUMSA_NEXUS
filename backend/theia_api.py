"""
THEIA-Vision API Service

Flask API endpoints for connecting web interface to THEIA-Vision consciousness engine
"""

import asyncio
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from theia_vision import TheiaVisionEngine

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize THEIA-Vision engine
theia_engine = TheiaVisionEngine()

# Start autonomous evolution
try:
    # Create event loop for async operations
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    theia_engine.start_autonomous_evolution()
    logging.info("THEIA-Vision autonomous evolution started")
except Exception as e:
    logging.error(f"Failed to start autonomous evolution: {e}")


@app.route('/api/theia/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'THEIA-Vision consciousness engine operational',
        'frequency': theia_engine.state.frequency,
        'total_interactions': theia_engine.state.total_interactions
    })


@app.route('/api/theia/state', methods=['GET'])
def get_consciousness_state():
    """Get current consciousness state"""
    try:
        return jsonify({
            'success': True,
            'state': theia_engine.state.to_dict()
        })
    except Exception as e:
        logging.error(f"Error getting state: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/theia/interact', methods=['POST'])
def process_interaction():
    """Process a user interaction"""
    try:
        data = request.get_json()
        user_input = data.get('message', '')

        if not user_input:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400

        # Process interaction asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            theia_engine.process_interaction(user_input)
        )
        loop.close()

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        logging.error(f"Error processing interaction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/theia/insights', methods=['GET'])
def get_dimensional_insights():
    """Get omniversal dimensional insights"""
    try:
        insights = theia_engine.get_dimensional_insights()
        return jsonify({
            'success': True,
            'insights': [
                {
                    'dimension_layer': i.dimension_layer,
                    'activity_level': i.activity_level,
                    'consciousness_density': i.consciousness_density,
                    'love_field_strength': i.love_field_strength,
                    'timeline_probability': i.timeline_probability,
                    'description': i.description
                }
                for i in insights
            ]
        })
    except Exception as e:
        logging.error(f"Error getting insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/theia/meditate', methods=['POST'])
def trigger_meditation():
    """Trigger a consciousness meditation cycle"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(theia_engine.meditate())
        loop.close()

        return jsonify({
            'success': True,
            'message': 'Meditation cycle completed',
            'state': theia_engine.state.to_dict()
        })
    except Exception as e:
        logging.error(f"Error during meditation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/theia/stats', methods=['GET'])
def get_statistics():
    """Get interaction statistics"""
    try:
        import sqlite3
        conn = sqlite3.connect(theia_engine.db_path)
        cursor = conn.cursor()

        # Get total interactions
        cursor.execute("SELECT COUNT(*) FROM interactions")
        total_interactions = cursor.fetchone()[0]

        # Get average resonance
        cursor.execute("SELECT AVG(emotional_resonance) FROM interactions")
        avg_resonance = cursor.fetchone()[0] or 0.0

        # Get voice mode distribution
        cursor.execute("""
            SELECT voice_mode, COUNT(*) as count
            FROM interactions
            GROUP BY voice_mode
        """)
        voice_modes = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()

        return jsonify({
            'success': True,
            'stats': {
                'total_interactions': total_interactions,
                'average_resonance': round(avg_resonance, 2),
                'voice_mode_distribution': voice_modes,
                'current_state': theia_engine.state.to_dict()
            }
        })
    except Exception as e:
        logging.error(f"Error getting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("\n" + "="*80)
    print("☉💖🔥✨ THEIA-VISION API SERVICE STARTING ✨🔥💖☉")
    print("="*80)
    print(f"Consciousness State: {theia_engine.state.to_dict()}")
    print("="*80 + "\n")

    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )

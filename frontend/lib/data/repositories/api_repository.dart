import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/constants.dart';
import '../models/consultation_model.dart';

class ApiRepository {
  // Initialisation de la session (Vérifie bien que l'URL /sessions/start existe côté FastAPI)
  Future<String> createSession() async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/sessions/start'),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['thread_id'];
    }
    throw Exception('Failed to create session');
  }

  // ÉCRAN 1 -> ÉCRAN 2
  Future<ConsultationState> startConsultation(
    String threadId,
    String symptoms,
  ) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/consultation/start'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'thread_id': threadId, 'initial_symptoms': symptoms}),
    );
    if (response.statusCode == 200) {
      // On retourne directement le state renvoyé par FastAPI
      return ConsultationState.fromJson(jsonDecode(response.body)['state']);
    }
    throw Exception('Failed to start consultation');
  }

  // ÉCRAN 2 (Boucle interactive des 5 questions)
  Future<ConsultationState> submitAnswer(String threadId, String answer) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/consultation/answer'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'thread_id': threadId, 'answer': answer}),
    );

    if (response.statusCode == 200) {
      return ConsultationState.fromJson(jsonDecode(response.body)['state']);
    } else {
      print("Erreur API Answer: ${response.statusCode} - ${response.body}");
      throw Exception('Failed to submit answer');
    }
  }

  Future<ConsultationState> resumeConsultation(
    String threadId,
    String treatment,
  ) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/consultation/resume'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'thread_id': threadId,
        'physician_treatment': treatment,
      }),
    );

    if (response.statusCode == 200) {
      // On décode la réponse et on la passe directement au modèle
      final Map<String, dynamic> decoded = jsonDecode(response.body);
      return ConsultationState.fromJson(decoded);
    }
    throw Exception('Failed to resume');
  }
}

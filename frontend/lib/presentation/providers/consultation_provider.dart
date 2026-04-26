import 'package:flutter/material.dart';
import '../../data/models/consultation_model.dart';
import '../../data/repositories/api_repository.dart';

class ConsultationProvider with ChangeNotifier {
  final ApiRepository _apiRepository = ApiRepository();
  ConsultationState? currentState;
  String? threadId;
  bool isLoading = false;

  // Démarre la consultation (Écran 1)
  Future<void> startConsultation(String symptoms) async {
    isLoading = true;
    notifyListeners();
    try {
      threadId = await _apiRepository.createSession();
      if (threadId != null) {
        currentState = await _apiRepository.startConsultation(
          threadId!,
          symptoms,
        );
      }
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  // Envoie une réponse (Écran 2)
  Future<void> submitPatientAnswer(String answer) async {
    isLoading = true;
    notifyListeners();
    try {
      currentState = await _apiRepository.submitAnswer(threadId!, answer);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> submitPhysicianReview(String treatment) async {
    if (threadId == null) return;
    isLoading = true;
    notifyListeners();
    try {
      // 1. On appelle l'API
      final newState = await _apiRepository.resumeConsultation(
        threadId!,
        treatment,
      );

      // 2. CRITIQUE : On s'assure que currentState contient TOUT, surtout le rapport
      this.currentState = newState;

      // DEBUG pour toi : regarde ta console VS Code après avoir cliqué
      print("DEBUG PROVIDER - Rapport reçu : ${currentState?.finalReport}");
    } catch (e) {
      print("ERREUR PROVIDER : $e");
    } finally {
      isLoading = false;
      notifyListeners(); // On prévient les écrans que la donnée est là
    }
  }

  void resetConsultation() {
    currentState = null;
    threadId = null;
    isLoading = false;
    notifyListeners();
  }
}

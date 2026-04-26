class ConsultationState {
  final List<dynamic> messages;
  final int questionCount;
  final String diagnosticSummary;
  final String interimCare;
  final String physicianTreatment;
  final String finalReport; // Doit correspondre à la clé du backend

  ConsultationState({
    required this.messages,
    required this.questionCount,
    required this.diagnosticSummary,
    required this.interimCare,
    required this.physicianTreatment,
    required this.finalReport,
  });

  factory ConsultationState.fromJson(Map<String, dynamic> json) {
    // Si le backend a enveloppé les données dans "state", on les extrait
    final Map<String, dynamic> data = json.containsKey('state')
        ? json['state']
        : json;

    return ConsultationState(
      messages: data['messages'] ?? [],
      questionCount: data['question_count'] ?? 0,
      diagnosticSummary: data['diagnostic_summary'] ?? '',
      interimCare: data['interim_care'] ?? '',
      physicianTreatment: data['physician_treatment'] ?? '',
      // On cherche agressivement le rapport final :
      finalReport: data['final_report'] ?? "",
    );
  }
}

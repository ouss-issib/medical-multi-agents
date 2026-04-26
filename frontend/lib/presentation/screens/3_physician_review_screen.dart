import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../providers/consultation_provider.dart';
import '4_final_report_screen.dart';

class PhysicianReviewScreen extends StatefulWidget {
  const PhysicianReviewScreen({super.key});

  @override
  State<PhysicianReviewScreen> createState() => _PhysicianReviewScreenState();
}

class _PhysicianReviewScreenState extends State<PhysicianReviewScreen> {
  final TextEditingController _treatmentController = TextEditingController();

  @override
  void dispose() {
    _treatmentController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<ConsultationProvider>(context);
    final state = provider.currentState;

    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text('Revue Médecin (HITL)'),
        backgroundColor: const Color(0xFF004D40),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSectionTitle(
              "Synthèse Clinique Préliminaire",
              Icons.summarize,
            ),
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: MarkdownBody(
                  data:
                      state?.diagnosticSummary ?? "Aucune synthèse disponible.",
                  styleSheet: MarkdownStyleSheet(
                    p: const TextStyle(fontSize: 15, height: 1.5),
                    strong: const TextStyle(color: Color(0xFF004D40)),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 25),

            _buildSectionTitle("Recommandation Intermédiaire (MCP)", Icons.api),
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              color: const Color(
                0xFFE0F2F1,
              ), // Fond légèrement teinté pour différencier le MCP
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Text(
                  state?.interimCare ?? "Aucune recommandation MCP.",
                  style: const TextStyle(
                    fontSize: 15,
                    color: Color(0xFF004D40),
                    fontStyle: FontStyle.italic,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 25),

            _buildSectionTitle(
              "Traitement ou Conduite à tenir",
              Icons.edit_note,
            ),
            TextField(
              controller: _treatmentController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: "Saisissez vos instructions médicales ici...",
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: BorderSide.none,
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(15),
                  borderSide: const BorderSide(
                    color: Color(0xFF00796B),
                    width: 2,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 35),

            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF004D40),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                  elevation: 3,
                ),
                onPressed: provider.isLoading
                    ? null
                    : () async {
                        if (_treatmentController.text.trim().isNotEmpty) {
                          await provider.submitPhysicianReview(
                            _treatmentController.text,
                          );
                          if (context.mounted) {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const FinalReportScreen(),
                              ),
                            );
                          }
                        }
                      },
                child: provider.isLoading
                    ? const SizedBox(
                        height: 24,
                        width: 24,
                        child: CircularProgressIndicator(
                          color: Colors.white,
                          strokeWidth: 2,
                        ),
                      )
                    : const Text(
                        "Valider et Générer le Rapport",
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  // Widget réutilisable pour les titres de section avec icônes
  Widget _buildSectionTitle(String title, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 12),
      child: Row(
        children: [
          Icon(icon, color: const Color(0xFF00796B), size: 22),
          const SizedBox(width: 10),
          Text(
            title,
            style: const TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 16,
              color: Color(0xFF004D40),
            ),
          ),
        ],
      ),
    );
  }
}

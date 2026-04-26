import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../providers/consultation_provider.dart';

class FinalReportScreen extends StatelessWidget {
  const FinalReportScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<ConsultationProvider>(context);
    final report = provider.currentState?.finalReport ?? "";

    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA), // Fond gris très clair pro
      appBar: AppBar(
        title: const Text(
          'Rapport Médical Final',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: const Color(0xFF004D40), // Teal Foncé
        elevation: 0,
        automaticallyImplyLeading: false, // Supprime le bouton retour
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            // Carte du Rapport
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
              child: Padding(
                padding: const EdgeInsets.all(25.0),
                child: MarkdownBody(
                  data: report,
                  styleSheet: MarkdownStyleSheet(
                    h1: const TextStyle(
                      color: Color(0xFF004D40),
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                    p: const TextStyle(
                      fontSize: 16,
                      height: 1.5,
                      color: Colors.black87,
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 30),

            // Bouton Nouvelle Consultation
            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.add_circle_outline, color: Colors.white),
                label: const Text(
                  "Nouvelle Consultation",
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF00796B),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
                onPressed: () {
                  provider.resetConsultation();
                  Navigator.of(context).popUntil((route) => route.isFirst);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

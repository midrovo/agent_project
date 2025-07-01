
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:project_app/models/product_model.dart';

class ProductService {
  final String baseUrl = 'https://616a-179-49-35-193.ngrok-free.app/api/v1/products';

  Future<List<Product>> fetchProducts() async {
    final response = await http.get(Uri.parse(baseUrl));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Product.fromJson(json)).toList();
    } else {
      throw Exception('Error fetching products. Status code: ${response.statusCode}');
    }
  }
}

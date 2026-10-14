// El producto punto de dos vectores de floats, dos veces: con un ciclo
// escalar y con instrucciones AVX que operan ocho floats por instrucción.
//
// Los valores son enteros pequeños y el vector tiene 2^20 posiciones, de
// modo que todas las sumas parciales son exactas en float y las dos versiones
// tienen que imprimir el mismo número.
#include <chrono>
#include <cstdio>
#include <immintrin.h>
#include <vector>

using namespace std;
using namespace std::chrono;

const size_t N = 1 << 20;
const int REPETICIONES = 200;

// Un producto y una suma por elemento, en secuencia.
float escalar(const float *a, const float *b, size_t n) {
  float suma = 0.0f;
  for (size_t i = 0; i < n; i++) suma += a[i] * b[i];
  return suma;
}

// TODO: de a ocho elementos por vuelta. Cargar ocho floats de a y ocho de b
// con _mm256_loadu_ps, multiplicarlos con _mm256_mul_ps y acumular en un
// registro __m256 con _mm256_add_ps. Al final, sumar las ocho posiciones del
// acumulador (reducción horizontal) y agregar los elementos que sobran cuando
// n no es múltiplo de ocho.
float con_avx(const float *a, const float *b, size_t n) {
  __m256 acc = _mm256_setzero_ps();
  for(size_t i = 0; i + 8 <= n; i += 8) {
    __m256 va = _mm256_loadu_ps(a + i);
    __m256 vb = _mm256_loadu_ps(b + i);
    __m256 vm = _mm256_mul_ps(va, vb);
    acc = _mm256_add_ps(acc, vm);
  }
  // Reducción horizontal
  __m128 hi = _mm256_extractf128_ps(acc, 1);
  __m128 lo = _mm256_castps256_ps128(acc);
  __m128 sum = _mm_add_ps(hi, lo);
  sum = _mm_hadd_ps(sum, sum);
  sum = _mm_hadd_ps(sum, sum);
  float resultado = _mm_cvtss_f32(sum);
  // Sumar los elementos restantes si n no es múltiplo de ocho
  for(size_t i = n - n % 8; i < n; i++) {
    resultado += a[i] * b[i];
  }
  return resultado;
}

int main() {
  vector<float> a(N), b(N);
  for (size_t i = 0; i < N; i++) {
    a[i] = (float)(i % 4);
    b[i] = (float)(i % 3);
  }

  float r1 = 0, r2 = 0;
  auto t0 = high_resolution_clock::now();
  for (int k = 0; k < REPETICIONES; k++) r1 = escalar(a.data(), b.data(), N);
  auto t1 = high_resolution_clock::now();
  for (int k = 0; k < REPETICIONES; k++) r2 = con_avx(a.data(), b.data(), N);
  auto t2 = high_resolution_clock::now();

  printf("escalar %.1f ms resultado %.0f\n",
         duration_cast<microseconds>(t1 - t0).count() / 1000.0, r1);
  printf("avx %.1f ms resultado %.0f\n",
         duration_cast<microseconds>(t2 - t1).count() / 1000.0, r2);
  return 0;
}

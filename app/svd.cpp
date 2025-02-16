#include <torch/torch.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <tuple>

namespace py = pybind11;

std::tuple<torch::Tensor, torch::Tensor, torch::Tensor> compute_svd(const torch::Tensor& input_tensor) {
    // Verificar que el tensor sea de 2 dimensiones
    if (input_tensor.dim() != 2) {
        throw std::runtime_error("El tensor de entrada debe ser bidimensional");
    }

    // Realizar la descomposición SVD
    torch::Tensor U, S, V;
    std::tie(U, S, V) = torch::svd(input_tensor);

    return std::make_tuple(U, S, V);
}

PYBIND11_MODULE(svd_module, m) {
    m.doc() = "Módulo para calcular la descomposición en valores singulares (SVD) usando PyTorch en C++";
    m.def("compute_svd", &compute_svd, "Función para calcular SVD",
          py::arg("input_tensor"));
}

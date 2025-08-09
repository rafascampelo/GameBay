// Este é o código JavaScript que será importado pelo index.html

// Função para mostrar uma mensagem de feedback ao usuário
function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.remove("opacity-0");
  toast.classList.add("opacity-100");
  setTimeout(() => {
    toast.classList.remove("opacity-100");
    toast.classList.add("opacity-0");
  }, 3000);
}

// Função para criar um card de jogo no HTML
function createGameCard(game) {
  const card = document.createElement("div");
  card.className =
    "bg-[#1a1f26] rounded-lg shadow-lg overflow-hidden transition-transform duration-300 hover:scale-105";

  // Verifica se a imagem existe, caso contrário, usa um placeholder
  const imageUrl =
    game.background_image ||
    `https://placehold.co/400x225/1a1f26/d1d5db?text=${encodeURIComponent(
      game.name
    )}`;

  card.innerHTML = `
        <img src="${imageUrl}" alt="${
    game.name
  }" class="w-full h-48 object-cover">
        <div class="p-4">
            <h3 class="text-xl font-bold text-gray-100">${game.name}</h3>
            <div class="mt-2 text-sm text-gray-400">
                <p><strong>Lançamento:</strong> ${game.released || "N/A"}</p>
                <p><strong>Gêneros:</strong> ${
                  game.genres.map((g) => g.name).join(", ") || "N/A"
                }</p>
            </div>
        </div>
    `;
  return card;
}

// Função para buscar a lista de jogos populares
async function fetchGames() {
  const gamesContainer = document.getElementById("games-container");
  gamesContainer.innerHTML =
    '<p class="text-center text-lg col-span-full">A carregar jogos...</p>';

  try {
    const gamesUrl = "/api/games";
    const gamesResponse = await fetch(gamesUrl);

    if (!gamesResponse.ok) {
      // Lança um erro se a resposta da API não for bem-sucedida (ex: 404, 500)
      throw new Error(`Erro na API: ${gamesResponse.status}`);
    }

    const gamesData = await gamesResponse.json();

    gamesContainer.innerHTML = ""; // Limpa a mensagem de carregamento
    if (gamesData.length > 0) {
      gamesData.forEach((game) => {
        const card = createGameCard(game);
        gamesContainer.appendChild(card);
      });
    } else {
      gamesContainer.innerHTML =
        '<p class="text-center text-lg col-span-full text-gray-400">Nenhum jogo encontrado.</p>';
    }
  } catch (error) {
    console.error("Erro ao buscar jogos populares:", error);
    gamesContainer.innerHTML = `<p class="text-center text-lg col-span-full text-red-500">Erro ao carregar jogos. Detalhes: ${error.message}</p>`;
  }
}

// Ao carregar a página, busca a lista de jogos
document.addEventListener("DOMContentLoaded", () => {
  fetchGames();
});

// Esta é a parte do JavaScript que será importada pelo index.html

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

  // Adiciona a imagem de fundo do jogo
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
            <button class="favorite-btn mt-4 w-full bg-[#3d424b] text-[#66d9ef] font-semibold py-2 px-4 rounded-md hover:bg-[#4a515c] transition-colors duration-300" data-game='${JSON.stringify(
              game
            )}'>
                Favoritar
            </button>
        </div>
    `;
  return card;
}

// Função para buscar a lista de jogos populares
async function fetchGames() {
  const gamesContainer = document.getElementById("games-container");
  gamesContainer.innerHTML =
    '<p class="text-center text-lg col-span-full">Carregando jogos...</p>';

  try {
    // A requisição para a rota '/api/games' que você vai criar no Flask
    const gamesUrl = "/api/games";
    const gamesResponse = await fetch(gamesUrl);
    if (!gamesResponse.ok)
      throw new Error("Não foi possível buscar a lista de jogos.");
    const gamesData = await gamesResponse.json();

    gamesContainer.innerHTML = ""; // Limpa a mensagem de carregamento
    gamesData.forEach((game) => {
      const card = createGameCard(game);
      gamesContainer.appendChild(card);
    });
  } catch (error) {
    console.error("Erro ao buscar jogos populares:", error);
    gamesContainer.innerHTML =
      '<p class="text-center text-lg col-span-full text-red-500">Erro ao carregar jogos. Tente novamente mais tarde.</p>';
  }
}

// Função para adicionar um jogo aos favoritos
async function addFavorite(gameData) {
  try {
    const response = await fetch("/api/add_favorite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(gameData),
    });
    const result = await response.json();
    if (result.success) {
      showToast(result.message);
    } else {
      showToast(result.message);
    }
  } catch (error) {
    console.error("Erro ao adicionar favorito:", error);
    showToast("Erro de conexão com o servidor.");
  }
}

// Função para buscar e exibir as recomendações
async function fetchRecommendations() {
  const recContainer = document.getElementById("recommendations-container");
  recContainer.innerHTML =
    '<p class="text-center text-lg col-span-full">Gerando recomendações...</p>';

  try {
    const response = await fetch("/api/recommendations");
    const recommendations = await response.json();

    recContainer.innerHTML = ""; // Limpa a mensagem de carregamento

    if (recommendations.success === false) {
      // Mensagem de erro da API, se não houver favoritos
      recContainer.innerHTML = `<p class="text-center text-lg col-span-full text-yellow-400">${recommendations.message}</p>`;
    } else {
      recommendations.forEach((game) => {
        const card = createGameCard(game);
        recContainer.appendChild(card);
      });
    }
  } catch (error) {
    console.error("Erro ao buscar recomendações:", error);
    recContainer.innerHTML =
      '<p class="text-center text-lg col-span-full text-red-500">Erro ao carregar recomendações. Tente novamente mais tarde.</p>';
  }
}

// Listener para o botão de Favoritar
document.addEventListener("click", (event) => {
  if (event.target.classList.contains("favorite-btn")) {
    // Pega os dados do jogo salvos no atributo 'data-game'
    const gameData = JSON.parse(event.target.getAttribute("data-game"));
    addFavorite(gameData);
  }
});

// Listener para o botão de Recomendações
document
  .getElementById("get-recommendations-btn")
  .addEventListener("click", fetchRecommendations);

// Ao carregar a página, busca a lista de jogos
document.addEventListener("DOMContentLoaded", () => {
  fetchGames();
});

#include "data.cpp"
#include <iostream>
#include <vector>
#include <time.h>
#include <stdlib.h>
#include <string>
#include <random>
#include <chrono>
#include <math.h>
#include <conio.h>
#include <algorithm>
#include <iomanip>


using namespace std::chrono;
using namespace std;

int myrandom (int i) { return std::rand()%i;}

struct Node {
    int x, y;
    int demand = 0;
    bool is_station = false;
    bool is_central_depot = false;
};

// vector<int> values = {732,915,38,5,994,319,197,499,552,740,609,545,757,262,468,892,726,604,126,939,44,811,150,500,688,536,12,203,423,293,113,122,732,545,466,30,763,990,728,481,712,630,136,549,616,191,265,319,369,309,958,884,489,173,922,849,17,814,13,853,595,927,636,145,528,889,391,620,355,666,351,271,6,921,608,892,693,309,71,974,915,904,377,591,751,329,264,260,500,404,867,820,135,291,455,955,837,440,825,125};
// vector<int> values = {60, 100, 120};
// vector<int> weights = {10, 20, 30};
// vector<int> weights{77,908,178,827,913,429,343,41,32,945,871,110,365,669,359,20,937,550,281,902,342,994,677,928,368,608,776,556,596,618,964,917,455,332,792,529,308,341,245,263,482,384,119,892,314,933,696,963,698,946,477,717,620,45,943,759,87,701,646,967,508,88,485,516,550,458,35,427,240,945,325,969,353,369,7,817,86,734,685,562,315,907,757,390,830,11,773,111,599,726,934,97,732,743,569,143,931,36,635,167};
// int capacities = 26396;
// int capacities = 50;
int capacities, num_vehicles, num_customers, num_stations, energy_capacity;
int individualSize, populationSize = 200;
double energy_consumption;
vector<int> values, weights;
vector<Node> node;
int randomfunc(int j) {
    return rand() % j;
}

#include <iostream>
#include <sstream>
using namespace std;
  
int extractIntegerWords(string str)
{
    stringstream ss;    
  
    /* Storing the whole string into string stream */
    ss << str;
  
    /* Running loop till the end of the stream */
    string temp;
    int found;
    while (!ss.eof()) {
  
        /* extracting word by word from stream */
        ss >> temp;
  
        /* Checking the given word is integer or not */
        if (stringstream(temp) >> found)
            return found;
  
        /* To save from space at the end of string */
        temp = "";
    }
}

void Generate(vector<vector<int>> &a, int file_index) {
    int sum_demand, sum_demand_2;
    vector<int> b;
    for (int i = 0; i < populationSize; i++) {
        
        b.clear();
        b.shrink_to_fit();
        for (int j = 0; j < individualSize; j++)
            b.push_back(j + 1);
        
        random_shuffle(b.begin(), b.end());
        random_shuffle(b.begin(), b.end(), randomfunc);
        
        // cout << "test\n";
        // for (int j = 0; j < individualSize; j++)
        //     cout << b[j] << " ";
        // cout << "\n";
        sum_demand = 0;
        sum_demand_2 = 0;
        int j = 0;
        int num_zero = 0;
        // cout << individualSize << "\n";
        int n = individualSize;
       
        while (j < n && num_zero < num_vehicles - 1) {
            sum_demand_2 += node[b[j]].demand;
            if (sum_demand <= capacities && sum_demand_2 > capacities && b[j - 1] != 0) {
                // cout << j << "\n";
                // cout << j << " test\n";
                n++;
                b.insert(b.begin() + j, 0);
                sum_demand = 0;
                sum_demand_2 = 0;
                j++;
                num_zero++;
                // for (int t = 0; t < n; t++)
                //     cout << b[t] << " ";
                // cout << "\n";
                
            }
            else sum_demand += node[b[j]].demand;
            j++;
        }
       
        n++;
        b.insert(b.begin(), 0);
        if (b[b.size() - 1] != 0 && num_zero < num_vehicles) {
            n++;
            b.insert(b.end(), 0);
            num_zero++;
        }
        
        int randNum;
  
       
        while (num_zero < num_vehicles) {
            do
                randNum  = rand() % ((b.size() - 2) - 2 + 1) + 2;
            while (b[randNum - 1] == 0 || b[randNum] == 0);
            b.insert(b.begin() + randNum, 0);
            num_zero++;
        }
        // for (int j = 0; j < b.size(); j++)
        //     cout << b[j] << " ";
        // cout << "\n/---------------------------/\n\n";
        a.push_back(b);
    }
}

void Print(const vector<vector<int>> &a, const int &m, const int &n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++)
            cout << a[i][j] << " ";
        cout << '\n';
    } 
}

vector<vector<int>> Crossover(vector<vector<int>> a, int file_index) {
    vector<vector<int>> b = a;
    vector<int> off1, off2;
    int i = 0, cnt, l, r, pos;
    while (i < populationSize - 1) {
        int randNum = rand() % (num_vehicles - 1 + 1) + 1;
        cnt = 0;
        // if (file_index == 1) {
        //     for (int j = 0; j < individualSize; j++)
        //         cout << b[i][j] << " ";
        //     cout << "\n";
        // }
        pos = 0;
        for (int j = 0; j < individualSize; j++) 
            if (b[i][j] == 0) {
                cnt++; 
                if (cnt == randNum) {
                    l = j;
                    auto it = b[i].begin() + j;
                    auto x = *it; 
                    b[i].erase(it);
                    b[i].insert(b[i].begin(), x);
                }
                else if (cnt == randNum + 1) {
                    break;
                }
            }
            else if (cnt == randNum) {
                auto it = b[i].begin() + j;
                auto x = *it; 
                b[i].erase(it);
                pos++;
                b[i].insert(b[i].begin() + pos, x);
            }

        off1 = b[i];
        b[i].erase(b[i].begin() + pos + 2, b[i].end());
        //Cha 2
        // for (int j = 0; j < individualSize; j++)
        //         cout << b[i + 1][j] << " ";
        //     cout << "\n";

        int pos2 = 0; 
        cnt = 0;
        randNum = rand() % (num_vehicles - 1 + 1) + 1;
        for (int j = 0; j < individualSize; j++) 
            if (b[i + 1][j] == 0) {
                cnt++; 
                if (cnt == randNum) {
                    l = j;
                    auto it = b[i + 1].begin() + j;
                    auto x = *it; 
                    b[i + 1].erase(it);
                    b[i + 1].insert(b[i + 1].begin(), x);
                }
                else if (cnt == randNum + 1) {
                    // r = j;
                    // auto it = b[i].begin() + j;
                    // auto x = *it; 
                    // b[i].erase(it);
                    // pos++;
                    // b[i].insert(b[i].begin() + pos, x);
                    break;
                }
            }
            else if (cnt == randNum) {
                auto it = b[i + 1].begin() + j;
                auto x = *it; 
                b[i + 1].erase(it);
                pos2++;
                b[i + 1].insert(b[i + 1].begin() + pos2, x);
            }
        
        // for (int j = 0; j < b[i].size(); j++)
        //     cout << b[i][j] << " ";
        // cout << "\n";


        
        off2 = b[i + 1];
        b[i + 1].erase(b[i + 1].begin() + pos2 + 2, b[i + 1].end());
        
        // for (int j = 0; j < b[i + 1].size(); j++)
        //     cout << b[i + 1][j] << " ";
        // cout << "\n";

        // for (int j = 0; j < off2.size(); j++)
        //     cout << off2[j] << " ";
        // cout << "\n";

        for (int j = 0; j < off2.size(); j++)
            if (find(b[i].begin(), b[i].end(), off2[j]) == b[i].end()) {
                b[i].push_back(off2[j]);
                // cout << off2[j] << " ";
            }

        for (int j = 0; j < off1.size(); j++)
            if (find(b[i + 1].begin(), b[i + 1].end(), off1[j]) == b[i + 1].end())
                b[i + 1].push_back(off1[j]);

        // for (int j = 0; j < b[i].size(); j++)
        //     cout << b[i][j] << " ";
        // cout << "\n";

        // for (int j = 0; j < b[i + 1].size(); j++)
        //     cout << b[i + 1][j] << " ";
        // cout << "\n";
        // cout << pos << "\n";

        b[i].insert(b[i].end(), 0);
        b[i + 1].insert(b[i + 1].end(), 0);

        
        for (int j = 0; j < num_vehicles - 2; j++) {
            do {
                // cout << randNum << 
                randNum = rand() % ((b[i].size() - 2) - (pos + 3) + 1) + (pos + 3);
                // cout << randNum << " " << b[i][randNum] << " " << b[i][randNum + 1] << "\n";
            } while (b[i][randNum - 1] == 0 || b[i][randNum] == 0);
            
           
            b[i].insert(b[i].begin() + randNum, 0);
            do {
                randNum = rand() % ((b[i + 1].size() - 2) - (pos2 + 3) + 1) + (pos2 + 3);
                // cout << randNum << " " << b[i + 1][randNum] << " " << b[i + 1][randNum + 1] << "\n";
            } while (b[i + 1][randNum - 1] == 0 || b[i + 1][randNum] == 0);
            // cout << randNum << "\n";
            b[i + 1].insert(b[i + 1].begin() + randNum, 0);
        }
        

        // cout << b[i].size() << "\n";
        // for (int j = 0; j < b[i].size(); j++)
        //     cout << b[i][j] << " ";
        // cout << "\n";

        // cout << b[i + 1].size() << "\n";
        // for (int j = 0; j < b[i + 1].size(); j++)
        //     cout << b[i + 1][j] << " ";
        // cout << "\n";
        // cout << i << "\n";
        // cout << "/-------------------/\n\n";
        

        i += 2;
    }
    return b;
}

vector<vector<int>> Pool(vector<vector<int>> a, vector<vector<int>> b) {
    vector<vector<int>> tm = a;
    tm.insert( tm.end(), b.begin(), b.end() );
    return tm;
}

double Euclidean(int x1, int y1, int x2, int y2) {
    return sqrt(pow(x1 - x2, 2) + pow (y1 - y2, 2));
}

double ValueMax(vector<int> a, int m1, int m2) {
    double total_distance = 0, dis, to_energy = energy_capacity, penelty_energy = 0;
    int penelty_capacity = 0, to_demand = 0;

    for (int i = 1; i < individualSize; i++) {
        dis = Euclidean(node[a[i]].x, node[a[i]].y, node[a[i - 1]].x, node[a[i - 1]].y);
        total_distance += dis;
        if (a[i] == 0) {
            penelty_capacity += m1 * max (to_demand - capacities, 0);
            to_demand = 0;
            penelty_energy += m2 * max(-to_energy, 0.0);
            to_energy = 0;
        }
        else {
            to_demand += node[a[i]].demand;
            to_energy -= energy_consumption * dis;
            if (node[a[i]].is_station)
                to_energy = energy_capacity;
            penelty_energy += m2 * max(-to_energy, 0.0);
        }
    }
    double z = energy_consumption * total_distance  + penelty_capacity + penelty_energy;
    // cout << "total_dis: " << fixed << setprecision(2) << total_distance << "\n";
    // cout << "z: " << fixed << setprecision(2) <<  z << "\n";
    // cout << "energy * total dis: " << fixed << setprecision(2) <<  energy_consumption * total_distance << "\n";
    // cout << "penelty capacity: " << fixed << setprecision(2) << penelty_capacity << "\n";
    // cout << "penelty energy: " << fixed << setprecision(2) << penelty_energy << "\n";

    double fit = 1 / z;
    return fit;
}
void TournamentSelection(vector<vector<int>> &parents, vector<double> &fitness_parents, vector<vector<int>> pool, vector<double> fitness_pool) {
    parents.clear();
    parents.shrink_to_fit();
    fitness_parents.clear();
    fitness_parents.shrink_to_fit();
    for (int k = 0; k < 2; k++) {
        vector<int> si(2 * populationSize);
        iota(si.begin() + 1, si.end(), 1);
        srand(unsigned(time(0)));
        random_shuffle (si.begin(),si.end());
        random_shuffle (si.begin(),si.end(), myrandom);
        double max_fitness = 0;
        int max_index = -1;

        for (int i = 0; i < 2 * populationSize; i++)
            if (i % 4 == 3) {
                parents.push_back(pool[max_index]);
                fitness_parents.push_back(fitness_pool[max_index]);
                max_fitness = 0;
                max_index = -1;
            }
            else if (fitness_pool[si[i]] >= max_fitness) {
                max_fitness = fitness_pool[si[i]];
                max_index = si[i];
            }
    }
}

bool Compare2Individual(vector<int> a, vector<int> b, int n) {
    for (int i = 0; i < n; i++)
        if (a[i] != b[i])
            return false;
        return true;
}

bool CheckConvergence(vector<vector<int>> a) {
    for (int i = 0; i < populationSize - 1; i++)
        if (!Compare2Individual(a[i], a[i + 1], individualSize))
            return false;
    return true;
}

void Mutation(vector<vector<int>> &pool, vector<int> &fitness_pool, double p) {



    // for (int i = 0; i < m; i++) 
    //     for (int j = 0; j < n; j++)
    //         if ((double) rand() / (RAND_MAX) < p) {
    //             if (pool[i][j] == 1) {
    //                 pool[i][j] = 0;
    //                 fitness_pool[i] -= values[j];
    //             }
    //             else {
    //                 pool[i][j] = 1;
    //                 fitness_pool[i] += values[j];
    //             }
    //         }
}



void ReadFile(int &individual_size) {
    string tm;
    
    node.clear();
    node.shrink_to_fit();
    for (int i = 0; i < 4; i++) {
        cin.ignore(500,'\n');
    }
    
    cin >> tm >> num_vehicles;
    cin >> tm >> num_customers;
    cin >> tm >> num_stations;
    cin >> tm >> capacities;
    cin >> tm >> energy_capacity;
    cin >> tm >> energy_consumption;

    individual_size = num_customers;
    for (int i = 0; i < 3; i++)
        cin.ignore(500, '\n');
    int id, x, y;
    // cin >> tm;
    // cout << tm;
    node.reserve(num_customers + num_stations + 1);
    for (int i = 0; i < num_customers + num_stations; i++)  {
        cin >> id >> x >> y;
        id--;
        node[id].x = x;
        node[id].y = y;
        // cout << id << " " << x << " " << y << "\n";
    }
    for (int i = 0; i < 2; i++)
        cin.ignore(500, '\n');
    int demand;
    for (int i = 0; i < num_customers; i++) {
        id--;
        cin >> id >> demand;
        node[id].demand = demand;
        // cout << id << " " << demand << "\n";
    }
    // cout << "test\n";
    cin >> tm;
    for (int i = 0; i < num_stations; i++) {
        id--;
        cin >> id;
        node[id].is_station = true;
    }
    // cout << id << "\n";
    // for (int i = 0; i < 2; i++)
        // cin.ignore(500, '\n');
    cin >> tm;
    id--;
    cin >> id;
    // cout << id << "\n";
    node[id].is_central_depot = true;
    // cout << id << "\n";
}

int main() {
    vector<string> inp = input_data();
    int v, w;
    double probMutation = 0.01;
    for (int file_index = 0; file_index < inp.size(); file_index++) {
        string file_name_tm = "evrp-benchmark-set/" + inp[file_index] + ".evrp";
        cout << file_name_tm << "\n";
        char* file_name = &file_name_tm[0];
        freopen(file_name, "r", stdin);
        ReadFile(individualSize);
        
        // vector<vector<int>> parents(populationSize + 5, vector<int>(individualSize, 0));
        vector<vector<int>> parents;
        vector<double> fitness_offspring, fitness_pool, fitness_parents;
        vector<vector<int>> offspring, pool;
        double time_step_in_iter;
        srand (time(NULL));
        Generate(parents, file_index);
        
        individualSize += num_vehicles + 1;
        // Print (parents, populationSize, individualSize);
        int ep = 0;
        // for (int j = 0; j < individualSize; j++)
        //     cout << parents[0][j] << " ";
        // cout << "\n";
        // cout << ValueMax(parents[0], 100, 50);
        
        auto start = high_resolution_clock::now();
        // while(!CheckConvergence(parents) && time_step_in_iter < 300) {
        while (ep < 50) {
            // cout << "Running...\n"; 
            
            offspring = Crossover(parents, file_index);
            // if (ep == 0 && file_index == 4)
            //     cout << "test\n";
            // offspring = TwopointCrossover(parents, populationSize, individualSize);
            pool = Pool(parents, offspring);
        
            fitness_parents.clear();
            fitness_parents.shrink_to_fit();
            fitness_offspring.clear();
            fitness_offspring.shrink_to_fit();
            for (int i = 0; i < populationSize; i++) {
                fitness_parents.push_back(ValueMax(parents[i], 10, 5));
                fitness_offspring.push_back(ValueMax(offspring[i], 10, 5));
            }
        
            fitness_pool = fitness_parents;
            fitness_pool.insert(fitness_pool.end(), fitness_offspring.begin(), fitness_offspring.end());
            
    //         // Mutation(pool, fitness_pool, populationSize * 2, individualSize, probMutation);
            TournamentSelection(parents, fitness_parents, pool, fitness_pool);
            
            ep++;
            
    //         // cout << time_step_in_iter << "\n";
    //         // if (time_step_in_iter > 10)
                // break;
        }
        
    //     auto stop = high_resolution_clock::now();
    //     auto duration = duration_cast<seconds>(stop - start);
        int computedValue = 0, indexIndividual = -1, totalWeight = 0;
        for (int i = 0; i < populationSize; i++) 
            if (fitness_parents[i] > computedValue) {
                computedValue = fitness_parents[i];
                indexIndividual = i;
            }
        
        cout << "solution: \n";
        for (int j = 0; j < individualSize; j++) 
            cout << parents[indexIndividual][j] << " ";
        cout << "\n";
        cout << "/---------------------/\n\n";
        

    //     // string output_filename= "output/Genetic_Algorithm/" + inp[file_index] + ".txt";
    //     // cout << output_filename << "\n";
    //     // char* outfile = &output_filename[0];
    //     // freopen(outfile, "w", stdout);
    //     cout << "File name: " << inp[file_index] << "\n";
    //     cout << "Number of items: " << individualSize << "\n";
        
    //     cout << "Total value: " << computedValue << "\n";
    //     cout << "Total weight: " << totalWeight << "\n";
    //     cout << "Capacity: " << capacities << "\n";
    //     cout << "Runtime: " << duration.count() << " seconds\n";
    //     cout << "Poluplation size: " << populationSize << "\n";
    //     cout << "Crossing: Uniform Crossover\n";
    //     // cout << "Crossing: Onepoint Crossover\n"; 
    //     cout << "Itertations: " << ep << "\n";
    //     // cout << "/---------------/\n\n";
        // return 0;
    }
}
